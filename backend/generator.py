import os
import time
import asyncio
from google import genai
from typing import List, Dict
from backend.config import GEMINI_API_KEY

# Use gemini-2.0-flash-lite for higher rate limits
FLASH_MODEL = "gemini-2.0-flash-lite"

# Initialize the 0.3.0 Client
client = None
if GEMINI_API_KEY:
    client = genai.Client(api_key=GEMINI_API_KEY)

async def generate_rag_response(query: str, results: List[Dict]):
    """
    Generate an AI shopping assistant response based on the search query and retrieved products.
    Includes retry logic for rate-limited API calls.
    """
    if not client:
        return "Gemini API Key not set. Cannot generate RAG response."
    
    if not results:
        return "No relevant products found in the catalog to generate an answer."
    
    # Context aggregation
    context_blocks = []
    for i, res in enumerate(results):
        p = res["product"]
        # p is a SQLAlchemy Product model object
        title = getattr(p, 'title', 'Unknown')
        price = getattr(p, 'price', 0.0)
        category = getattr(p, 'category', 'General')
        description = getattr(p, 'description', '')
        features = getattr(p, 'features', []) or []
        rating = getattr(p, 'rating', 0.0)

        context_blocks.append(
            f"Result {i+1}:\n"
            f"Title: {title}\n"
            f"Price: ${price}\n"
            f"Category: {category}\n"
            f"Description: {description}\n"
            f"Features: {', '.join(features) if features else 'N/A'}\n"
            f"Rating: {rating}/5\n"
        )
        
    context_str = "\n---\n".join(context_blocks)
    
    prompt_text = f"""User Query: {query}

Retrieved Catalog Context:
{context_str}

Instructions:
Answer the user query as a professional shopping assistant. 
Use ONLY the provided context above. 
Recommend specific products from the context if multiple options are available.
Include prices and ratings.
If nothing is relevant, say so politely."""
    
    # Retry logic for rate limits
    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = client.models.generate_content(
                model=FLASH_MODEL,
                contents=prompt_text
            )
            
            if hasattr(response, 'text') and response.text:
                return response.text
            
            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
                
            return "I found some products but couldn't generate a summary. Please see the list below."
            
        except Exception as e:
            error_str = str(e)
            print(f"RAG generation attempt {attempt+1}/{max_retries} failed: {error_str[:150]}")
            
            if "RESOURCE_EXHAUSTED" in error_str or "429" in error_str or "retryDelay" in error_str:
                if attempt < max_retries - 1:
                    wait_time = (attempt + 1) * 10  # 10s, 20s, 30s
                    print(f"Rate limited. Waiting {wait_time}s before retry...")
                    await asyncio.sleep(wait_time)
                    continue
            
            # Non-retryable error or final attempt
            return f"I found the following products for you. (AI summary temporarily unavailable due to API rate limits.)"
    
    return "I found some products but couldn't generate a summary due to rate limits. Please see the list below."
