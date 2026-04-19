import os
from sqlalchemy import create_engine, text, inspect
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    print("❌ Error: DATABASE_URL not set.")
    exit(1)

print(f"Connecting to: {DATABASE_URL}")
engine = create_engine(DATABASE_URL)

try:
    with engine.connect() as conn:
        # Check tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"Tables: {tables}")
        
        if "products" in tables:
            result = conn.execute(text("SELECT count(*) FROM products"))
            count = result.scalar()
            print(f"Row count in 'products': {count}")
            
            if count > 0:
                result = conn.execute(text("SELECT product_id, title FROM products LIMIT 5"))
                print("First 5 products:")
                for row in result:
                    print(f" - {row[0]}: {row[1]}")
        else:
            print("❌ Error: 'products' table does not exist.")
            
except Exception as e:
    print(f"❌ Database error: {e}")
