import json
import asyncio
import os
import sys
from pinecone import Pinecone

# Add the project root to sys.path so we can import from backend
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal, engine, Base
from backend import crud, schemas, models
from backend.config import PINECONE_API_KEY, PINECONE_INDEX_NAME

async def run_loading():
    print("--- 1. Cleaning Database & Vector Store ---")
    
    # Clean PostgreSQL
    print("Dropping existing tables to ensure a clean slate...")
    Base.metadata.drop_all(bind=engine)
    print("Recreating tables...")
    Base.metadata.create_all(bind=engine)
    
    # Clean Pinecone
    try:
        pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
        index_name = os.getenv("PINECONE_INDEX_NAME")
        index = pc.Index(index_name)
        print(f"Clearing Pinecone index '{index_name}'...")
        index.delete(delete_all=True)
    except Exception as e:
        print(f"Warn: Could not clear Pinecone index: {e}")

    db = SessionLocal()
    
    # Path to products.json at project root
    json_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "products.json")
    if not os.path.exists(json_path):
        print(f"❌ Error: {json_path} not found.")
        return

    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # Check if it's a list or a dict with "products" key
        if isinstance(data, dict) and "products" in data:
            products = data["products"]
        elif isinstance(data, list):
            products = data
        else:
            print("❌ Error: Invalid products.json format.")
            return

    print(f"--- 2. Seeding {len(products)} products ---")
    
    for i, p_data in enumerate(products):
        print(f"[{i+1}/{len(products)}] Ingesting {p_data['title']}...")
        product_create = schemas.ProductCreate(**p_data)
        try:
            await crud.create_product(db, product_create)
        except Exception as e:
            print(f"❌ Error loading {p_data['title']}: {e}")
            
    print("--- Seeding Complete ---")
    db.close()

if __name__ == "__main__":
    asyncio.run(run_loading())
