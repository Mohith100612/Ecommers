import os
import json
import numpy as np
import google.generativeai as genai
from typing import List, Dict

# Configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    print("❌ ERROR: GEMINI_API_KEY environment variable is not set.")
    print("Please set it using: set GEMINI_API_KEY=your_key_here")
    exit(1)

genai.configure(api_key=GEMINI_API_KEY)

# Constants
EMBEDDING_MODEL = "models/text-embedding-004"
LLM_MODEL_NAME = "gemini-1.5-flash"
PRODUCTS_FILE = "products.json"

class ProductSearchApp:
    def __init__(self):
        self.products = []
        self.product_embeddings = None
        self.llm = genai.GenerativeModel(LLM_MODEL_NAME)
        
    def load_data(self):
        """Loads products from the JSON file and prepares them for embedding."""
        print(f"--- Loading data from {PRODUCTS_FILE} ---")
        try:
            with open(PRODUCTS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.products = data.get("products", [])
            print(f"Loaded {len(self.products)} products.")
        except FileNotFoundError:
            print(f"❌ ERROR: {PRODUCTS_FILE} not found.")
            exit(1)
        except Exception as e:
            print(f"❌ ERROR loading file: {e}")
            exit(1)

    def preprocess_text(self, product: Dict) -> str:
        """Combines product fields into a single string for embedding."""
        title = product.get("title", "")
        category = product.get("category", "")
        description = product.get("description", "")
        features = " ".join(product.get("features", []))
        return f"{title} {category} {description} {features}".strip()

    def generate_embeddings(self):
        """Generates embeddings for all products using Gemini."""
        print(f"--- Generating embeddings using {EMBEDDING_MODEL} ---")
        texts = [self.preprocess_text(p) for p in self.products]
        
        # Batch processing (Gemini supports up to 100 per call for some models, 
        # but we'll use a safe batch size)
        batch_size = 50
        all_embeddings = []
        
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i : i + batch_size]
            print(f"Processing batch {i//batch_size + 1}...")
            try:
                response = genai.embed_content(
                    model=EMBEDDING_MODEL,
                    content=batch_texts,
                    task_type="retrieval_document"
                )
                all_embeddings.extend(response['embedding'])
            except Exception as e:
                print(f"❌ ERROR generating embeddings: {e}")
                exit(1)
                
        self.product_embeddings = np.array(all_embeddings)
        print("Embeddings generated successfully.\n")

    def get_query_embedding(self, query: str) -> np.ndarray:
        """Generates embedding for the user search query."""
        try:
            response = genai.embed_content(
                model=EMBEDDING_MODEL,
                content=query,
                task_type="retrieval_query"
            )
            return np.array(response['embedding'])
        except Exception as e:
            print(f"❌ ERROR generating query embedding: {e}")
            return np.zeros(768) # Fallback to zero vector

    def calculate_similarity(self, query_vector: np.ndarray) -> np.ndarray:
        """
        Manually computes cosine similarity between query and all products.
        Formula: dot(A, B) / (||A|| * ||B||)
        """
        # Ensure query_vector is 1D
        query_vector = query_vector.flatten()
        
        # Dot product: (N, dim) . (dim,) -> (N,)
        dot_products = np.dot(self.product_embeddings, query_vector)
        
        # Norms
        norm_query = np.linalg.norm(query_vector)
        norm_products = np.linalg.norm(self.product_embeddings, axis=1)
        
        # Cosine similarity
        similarities = dot_products / (norm_query * norm_products + 1e-9) # small epsilon
        return similarities

    def search(self, query: str, top_k: int = 5):
        """Performs semantic search and returns top_k results."""
        query_vector = self.get_query_embedding(query)
        similarities = self.calculate_similarity(query_vector)
        
        # Get indices of top_k results
        top_indices = np.argsort(similarities)[::-1][:top_k]
        
        results = []
        for idx in top_indices:
            results.append({
                "product": self.products[idx],
                "score": float(similarities[idx])
            })
        return results

    def generate_rag_answer(self, query: str, results: List[Dict]):
        """Generates a final answer using the retrieved products as context."""
        context_parts = []
        for i, res in enumerate(results):
            p = res["product"]
            context_parts.append(
                f"Product {i+1}: {p['title']}\n"
                f"Category: {p['category']}\n"
                f"Price: ${p['price']}\n"
                f"Rating: {p['rating']}/5\n"
                f"Description: {p['description']}\n"
                f"Features: {', '.join(p['features'])}\n"
            )
        
        context_str = "\n---\n".join(context_parts)
        
        prompt = f"""
        User Query: {query}

        Retrieved Catalog Products:
        {context_str}

        Instructions:
        Using ONLY the retrieved products above, answer the user's question. 
        If none of the products strictly match, provide the closest recommendations from the list.
        Include details like price and key features to help the user decide.
        Be professional and helpful.
        """
        
        try:
            response = self.llm.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating answer: {e}"

    def run(self):
        """CLI main loop."""
        self.load_data()
        self.generate_embeddings()
        
        print("💡 Semantic Search Ready! Type 'exit' to quit.")
        
        while True:
            query = input("\n🔍 Enter your product search (e.g., 'best gaming setup'): ").strip()
            if not query or query.lower() == 'exit':
                print("Goodbye!")
                break
            
            print(f"Searching for: '{query}'...")
            results = self.search(query)
            
            print("\n--- TOP 5 RELEVANT PRODUCTS ---")
            for i, res in enumerate(results):
                p = res["product"]
                score = res["score"]
                print(f"{i+1}. {p['title']}")
                print(f"   Category: {p['category']} | Price: ${p['price']} | Rating: {p['rating']}⭐")
                print(f"   Similarity Score: {score:.4f}")
                print("-" * 40)
            
            print("\n🤖 AI SHOPPING ASSISTANT:")
            answer = self.generate_rag_answer(query, results)
            print(answer)
            print("=" * 60)

if __name__ == "__main__":
    app = ProductSearchApp()
    app.run()
