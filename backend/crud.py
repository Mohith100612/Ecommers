from sqlalchemy.orm import Session
from backend import models, schemas, ingest, vector_store
from fastapi import BackgroundTasks

def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()

def get_product_by_pid(db: Session, p_id: str):
    return db.query(models.Product).filter(models.Product.product_id == p_id).first()

def get_products(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Product).offset(skip).limit(limit).all()

async def create_product(db: Session, product: schemas.ProductCreate):
    # Process for vector store
    img_desc = await ingest.process_product_for_vector_store(product.dict())
    
    db_product = models.Product(
        product_id=product.product_id,
        title=product.title,
        category=product.category,
        brand=product.brand,
        price=product.price,
        rating=product.rating,
        review_count=product.review_count,
        description=product.description,
        features=product.features,
        image_url=product.image_url,
        image_description=img_desc
    )
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

async def delete_product(db: Session, p_id: str):
    product = get_product_by_pid(db, p_id)
    if product:
        # Delete from Pinecone
        vector_store.delete_vector(p_id)
        # Delete from DB
        db.delete(product)
        db.commit()
        return True
    return False

async def update_product(db: Session, p_id: str, product_update: schemas.ProductUpdate):
    db_product = get_product_by_pid(db, p_id)
    if not db_product:
        return None
    
    update_data = product_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    # Re-process if metadata changes
    # Re-embed for simplicity in this case
    img_desc = await ingest.process_product_for_vector_store(db_product.__dict__)
    db_product.image_description = img_desc
    
    db.commit()
    db.refresh(db_product)
    return db_product
