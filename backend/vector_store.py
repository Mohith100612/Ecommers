import time
from pinecone import Pinecone, ServerlessSpec
from backend.config import PINECONE_API_KEY, PINECONE_INDEX_NAME
INDEX_NAME = PINECONE_INDEX_NAME
DIMENSION = 3072 # For google gemini-embedding-2-preview

if not PINECONE_API_KEY:
    print("⚠️ WARNING: PINECONE_API_KEY not set. Vector search will fail.")

pc = None
index = None

def get_index():
    global pc, index
    if index:
        return index
    
    if not PINECONE_API_KEY:
        return None

    pc = Pinecone(api_key=PINECONE_API_KEY)
    
    # Check if index exists, else create
    if INDEX_NAME not in pc.list_indexes().names():
        pc.create_index(
            name=INDEX_NAME,
            dimension=DIMENSION,
            metric="cosine",
            spec=ServerlessSpec(
                cloud='aws', 
                region='us-east-1'
            )
        )
        # Wait for index to be ready
        while not pc.describe_index(INDEX_NAME).status['ready']:
            time.sleep(1)
            
    index = pc.Index(INDEX_NAME)
    return index

def upsert_vector(id: str, vector: list, metadata: dict):
    idx = get_index()
    if idx:
        idx.upsert(vectors=[(str(id), vector, metadata)])

def delete_vector(id: str):
    idx = get_index()
    if idx:
        idx.delete(ids=[str(id)])

def query_vectors(vector: list, top_k: int = 5, filter: dict = None):
    idx = get_index()
    if idx:
        return idx.query(
            vector=vector,
            top_k=top_k,
            include_metadata=True,
            filter=filter
        )
    return {"matches": []}
