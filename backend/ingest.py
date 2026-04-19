import httpx
from google import genai
from google.genai import types
from typing import List, Dict, Optional
from backend.vector_store import upsert_vector
from backend.config import GEMINI_API_KEY

EMBEDDING_MODEL = "gemini-embedding-2-preview" 

# Initialize the new 0.3.0 Client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

async def get_image_data(image_url: str) -> Optional[bytes]:
    """Helper to download image data."""
    if not image_url:
        return None
    try:
        async with httpx.AsyncClient() as client_http:
            resp = await client_http.get(image_url)
            return resp.content
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None

async def get_multimodal_embedding(text: str, image_bytes: Optional[bytes] = None) -> List[float]:
    """
    Generate 3072-dim embedding using gemini-embedding-2-preview.
    Supports native multimodal input via google-genai 0.3.0.
    """
    if not client:
        return [0.0] * 3072
    
    try:
        # Construct content properly for 0.3.0 SDK
        parts = []
        if text:
            parts.append(types.Part.from_text(text=text))
        if image_bytes:
            parts.append(types.Part.from_bytes(data=image_bytes, mime_type="image/jpeg"))
            
        result = client.models.embed_content(
            model=EMBEDDING_MODEL,
            contents=[types.Content(parts=parts)]
        )
        return result.embeddings[0].values
    except Exception as e:
        print(f"Error generating multimodal embedding: {e}")
        return [0.0] * 3072

async def process_product_for_vector_store(product_data: Dict):
    """
    Ingestion pipeline:
    1. Fetch image
    2. Build metadata text
    3. Generate NATIVE Multimodal embedding
    4. Upsert to Pinecone
    """
    img_url = product_data.get("image_url")
    img_bytes = await get_image_data(img_url)
    
    # Metadata text
    features_str = ", ".join(product_data.get("features", []))
    metadata_text = (
        f"Title: {product_data.get('title')}\n"
        f"Category: {product_data.get('category')}\n"
        f"Description: {product_data.get('description')}\n"
        f"Features: {features_str}"
    )
    
    vector = await get_multimodal_embedding(metadata_text, img_bytes)
    
    # Metadata for Pinecone filtering/display
    metadata = {
        "product_id": str(product_data.get("product_id")),
        "title": product_data.get("title"),
        "category": product_data.get("category"),
        "price": float(product_data.get("price", 0.0)),
        "rating": float(product_data.get("rating", 0.0)),
        "image_url": img_url
    }
    
    upsert_vector(product_data.get("product_id"), vector, metadata)
    return "Optimized via Native Multimodal Embedding"
