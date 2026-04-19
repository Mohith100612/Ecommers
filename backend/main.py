from fastapi import FastAPI, Depends, HTTPException, Query, status, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from backend import crud, models, schemas, database, retriever, generator

# Create DB tables
models.Base.metadata.create_all(bind=database.engine)

app = FastAPI(title="Multimodal RAG E-commerce API")

# CORS configuration
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173",  # Default Vite port
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # More permissive for debugging
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    import traceback
    print(f"GLOBAL ERROR: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={"message": str(exc), "traceback": traceback.format_exc()},
    )

# Endpoints

@app.post("/products", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(product: schemas.ProductCreate, db: Session = Depends(database.get_db)):
    db_product = crud.get_product_by_pid(db, product.product_id)
    if db_product:
        raise HTTPException(status_code=400, detail="Product ID already registered")
    return await crud.create_product(db=db, product=product)

@app.get("/products", response_model=List[schemas.Product])
def read_products(skip: int = 0, limit: int = 100, db: Session = Depends(database.get_db)):
    return crud.get_products(db, skip=skip, limit=limit)

@app.get("/products/{product_id}", response_model=schemas.Product)
def read_product(product_id: str, db: Session = Depends(database.get_db)):
    db_product = crud.get_product_by_pid(db, product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.put("/products/{product_id}", response_model=schemas.Product)
async def update_product(product_id: str, product: schemas.ProductUpdate, db: Session = Depends(database.get_db)):
    db_product = await crud.update_product(db, p_id=product_id, product_update=product)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    return db_product

@app.delete("/products/{product_id}")
async def delete_product(product_id: str, db: Session = Depends(database.get_db)):
    success = await crud.delete_product(db, p_id=product_id)
    if not success:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"message": "Product deleted successfully"}

@app.post("/search", response_model=schemas.SearchResponse)
async def search_catalog(
    query_text: str = Query(..., description="Semantic search query"),
    image_url: Optional[str] = Query(None, description="Optional image URL for visual search"),
    top_k: int = Query(100, description="Number of results to retrieve from vector store"),
    category: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    db: Session = Depends(database.get_db)
):
    # Retrieve
    matches = await retriever.search_products(
        db, 
        query_text=query_text, 
        image_url=image_url, 
        top_k=top_k,
        category=category,
        min_price=min_price,
        max_price=max_price
    )
    
    # Generate RAG answer
    answer = await generator.generate_rag_response(query_text, matches)
    
    return {
        "results": matches,
        "answer": answer
    }
