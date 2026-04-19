import asyncio
import os
import json
from typing import List, Dict
from backend import retriever, database, schemas, database as db_config
from sqlalchemy.orm import Session

# Sample Ground Truth for Evaluation
EVAL_CASES = [
    {
        "query": "high-end noise cancelling headphones for travel",
        "relevant_ids": ["WH001", "WH002", "WH003"]
    },
    {
        "query": "mechanical keyboard with tactile switches",
        "relevant_ids": ["MK001", "MK002", "MK003"]
    },
    {
        "query": "stability running shoes for overpronators",
        "relevant_ids": ["RS003", "RS005"]
    }
]

def calculate_precision_at_k(actual_ids: List[str], relevant_ids: List[str], k: int = 5):
    actual_k = actual_ids[:k]
    hits = len(set(actual_k) & set(relevant_ids))
    return hits / k

def calculate_mrr(actual_ids: List[str], relevant_ids: List[str]):
    for i, p_id in enumerate(actual_ids):
        if p_id in relevant_ids:
            return 1 / (i + 1)
    return 0

async def run_evaluation():
    db = db_config.SessionLocal()
    
    total_p5 = 0
    total_mrr = 0
    
    report_lines = ["# Search Evaluation Report\n"]
    
    for case in EVAL_CASES:
        query = case["query"]
        relevant = case["relevant_ids"]
        
        matches = await retriever.search_products(db, query, top_k=5)
        actual_ids = [m["product"].product_id for m in matches]
        
        p5 = calculate_precision_at_k(actual_ids, relevant, k=5)
        mrr = calculate_mrr(actual_ids, relevant)
        
        total_p5 += p5
        total_mrr += mrr
        
        report_lines.append(f"### Query: '{query}'")
        report_lines.append(f"- Relevant IDs: {relevant}")
        report_lines.append(f"- Retrieved IDs: {actual_ids}")
        report_lines.append(f"- **Precision@5**: {p5:.2f}")
        report_lines.append(f"- **MRR**: {mrr:.2f}\n")
        
    avg_p5 = total_p5 / len(EVAL_CASES)
    avg_mrr = total_mrr / len(EVAL_CASES)
    
    report_lines.append("## Summary Metrics")
    report_lines.append(f"- **Average Precision@5**: {avg_p5:.2f}")
    report_lines.append(f"- **Average MRR**: {avg_mrr:.2f}")
    
    # Save results
    os.makedirs("results", exist_ok=True)
    with open("results/eval_report.md", "w") as f:
        f.write("\n".join(report_lines))
        
    print(f"✅ Evaluation Complete. Average Precision@5: {avg_p5:.2f}, Average MRR: {avg_mrr:.2f}")
    print("Report saved to results/eval_report.md")
    db.close()

if __name__ == "__main__":
    asyncio.run(run_evaluation())
