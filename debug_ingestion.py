import sys
import os
import traceback
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session

# Add project root to path
sys.path.append(os.getcwd())

from backend.database import DATABASE_URL, Base, engine, SessionLocal
from backend import models, schemas, crud

async def debug_ingestion():
    try:
        # 1. Check connection
        with engine.connect() as conn:
            print("Successfully connected to Postgres.")
            
        # 2. Try to drop and recreate for fresh slate
        print("Dropping existing tables to ensure schema sync...")
        Base.metadata.drop_all(bind=engine)
        print("Creating tables...")
        Base.metadata.create_all(bind=engine)
        print("Tables created.")
        
        # 3. Try to insert ONE product
        db = SessionLocal()
        sample_p = {
            "product_id": "TEST001",
            "category": "Test",
            "title": "Test Product",
            "brand": "Test Brand",
            "price": 10.0,
            "rating": 5.0,
            "review_count": 1,
            "description": "Test desc",
            "features": ["f1"],
            "image_url": "https://example.com/img.jpg"
        }
        p_create = schemas.ProductCreate(**sample_p)
        print("Attempting to insert one product...")
        await crud.create_product(db, p_create)
        print("Successfully inserted one product.")
        db.close()
        
    except Exception as e:
        print("DEBUG INGESTION FAILED:")
        traceback.print_exc()

if __name__ == "__main__":
    import asyncio
    asyncio.run(debug_ingestion())
