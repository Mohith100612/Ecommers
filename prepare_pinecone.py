import os
import time
from pinecone import Pinecone, ServerlessSpec
from dotenv import load_dotenv

# Ensure we load the .env from the project root
env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
INDEX_NAME = os.getenv("PINECONE_INDEX_NAME", "ecommers")
DIMENSION = 3072 # For google gemini-embedding-2-preview

def create_index():
    print(f"--- 1. Initializing Pinecone (Key: {PINECONE_API_KEY[:5]}...) ---")
    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists, else create
    current_indexes = [i.name for i in pc.list_indexes()]
    if INDEX_NAME not in current_indexes:
        print(f"Creating index '{INDEX_NAME}' with dimension {DIMENSION}...")
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(cloud='aws', region='us-east-1')
        )
        # Wait for index to be ready
        print("Waiting for index to be ready...")
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(1)
        print("Index ready.")
    else:
        # Check if dimension matches
        desc = pc.describe_index(INDEX_NAME)
        if desc.dimension != DIMENSION:
            print(f"⚠️ Index '{INDEX_NAME}' exists but dimension is {desc.dimension} (Expected {DIMENSION}).")
            print("Deleting and recreating index...")
            pc.delete_index(INDEX_NAME)
            pc.create_index(
                name=INDEX_NAME,
                dimension=DIMENSION,
                metric="cosine",
                spec=ServerlessSpec(cloud='aws', region='us-east-1')
            )
            while not pc.describe_index(INDEX_NAME).status['ready']:
                time.sleep(1)
            print("Index recreated and ready.")
        else:
            print(f"Index '{INDEX_NAME}' already exists and matches expected dimension.")

if __name__ == "__main__":
    create_index()
