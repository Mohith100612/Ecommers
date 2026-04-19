import requests
import sys
import io

# Fix Windows console encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 60)
print("MULTIMODAL RAG E-COMMERCE - SYSTEM VERIFICATION")
print("=" * 60)

# Test 1: Products API
print("\n--- TEST 1: GET /products ---")
try:
    r = requests.get("http://localhost:8000/products?limit=100")
    r.raise_for_status()
    products = r.json()
    print(f"  [PASS] Total products in DB: {len(products)}")
    if len(products) > 0:
        print(f"  Sample: {products[0]['title']} (${products[0]['price']})")
except Exception as e:
    print(f"  [FAIL] {e}")

# Test 2: Search API
print("\n--- TEST 2: POST /search (Sony Headphones) ---")
try:
    r = requests.post(
        "http://localhost:8000/search",
        params={"query_text": "Sony noise cancelling headphones", "top_k": 3}
    )
    r.raise_for_status()
    data = r.json()
    print(f"  [PASS] Results returned: {len(data['results'])}")
    for res in data["results"]:
        p = res["product"]
        print(f"     - {p['title']} | ${p['price']} | Score: {res['score']:.3f}")
    
    answer = data.get("answer", "")
    if "error" in answer.lower() or "sorry" in answer.lower() or "encountered" in answer.lower():
        print(f"  [WARN] AI Answer has error: {answer[:150]}...")
    elif len(answer) > 20:
        print(f"  [PASS] AI Answer generated ({len(answer)} chars):")
        print(f"         {answer[:300]}...")
    else:
        print(f"  [WARN] AI Answer too short: {answer}")
except Exception as e:
    print(f"  [FAIL] {e}")

# Test 3: Another search
print("\n--- TEST 3: POST /search (running shoes) ---")
try:
    r = requests.post(
        "http://localhost:8000/search",
        params={"query_text": "comfortable running shoes for marathon", "top_k": 3}
    )
    r.raise_for_status()
    data = r.json()
    print(f"  [PASS] Results returned: {len(data['results'])}")
    for res in data["results"]:
        p = res["product"]
        print(f"     - {p['title']} | ${p['price']} | Score: {res['score']:.3f}")
    answer = data.get("answer", "")
    if "error" in answer.lower() or "sorry" in answer.lower() or "encountered" in answer.lower():
        print(f"  [WARN] AI Answer has error: {answer[:150]}...")
    elif len(answer) > 20:
        print(f"  [PASS] AI Answer generated ({len(answer)} chars):")
        print(f"         {answer[:300]}...")
    else:
        print(f"  [WARN] AI Answer too short: {answer}")
except Exception as e:
    print(f"  [FAIL] {e}")

print("\n" + "=" * 60)
print("VERIFICATION COMPLETE")
print("=" * 60)
