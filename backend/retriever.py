from typing import Optional, List, Dict
from backend.vector_store import query_vectors
from backend.ingest import get_multimodal_embedding, get_image_data
from backend import models, schemas
from sqlalchemy.orm import Session

# Absolute minimum score — anything below this is never relevant
ABSOLUTE_MIN_SCORE = 0.35

# If the top result's score is above this, use dynamic gap detection
# to find where relevant results end and noise begins
SCORE_DROP_RATIO = 0.75  # Cut off results below 75% of top score


async def search_products(
    db: Session, 
    query_text: str, 
    image_url: Optional[str] = None, 
    top_k: int = 100,
    category: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """
    Search products using multimodal query embedding.
    Uses dynamic relevance filtering: returns all products that are
    within 75% of the top result's score, ensuring only truly
    related items are returned.
    """
    img_bytes = None
    if image_url:
        img_bytes = await get_image_data(image_url)
    
    # Generate query embedding
    query_vector = await get_multimodal_embedding(query_text, img_bytes)
    
    # Build filter for Pinecone
    pc_filter = {}
    if category:
        pc_filter["category"] = {"$eq": category}
    
    if min_price is not None or max_price is not None:
        pc_filter["price"] = {}
        if min_price is not None:
            pc_filter["price"]["$gte"] = min_price
        if max_price is not None:
            pc_filter["price"]["$lte"] = max_price
            
    # Search Pinecone (fetch all, filter later)
    search_results = query_vectors(query_vector, top_k=top_k, filter=pc_filter if pc_filter else None)
    
    matches = search_results.get("matches", [])
    if not matches:
        return []
    
    # Dynamic threshold: use the top score to determine cutoff
    top_score = float(matches[0].get("score", 0.0))
    dynamic_threshold = max(ABSOLUTE_MIN_SCORE, top_score * SCORE_DROP_RATIO)
    
    final_matches = []
    for match in matches:
        score = float(match.get("score", 0.0))
        if score < dynamic_threshold:
            break  # Results are sorted by score, so we can stop early
        
        p_id = match.get("id")
        db_product = db.query(models.Product).filter(models.Product.product_id == p_id).first()
        if db_product:
            final_matches.append({
                "product": db_product,
                "score": score
            })
            
    return final_matches
