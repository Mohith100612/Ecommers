import requests, time

time.sleep(3)  # Wait for backend reload

queries = ["laptop", "wireless headphones", "running shoes", "skincare"]

for q in queries:
    r = requests.post('http://localhost:8000/search', params={'query_text': q, 'top_k': 100})
    data = r.json()
    results = data['results']
    
    print(f"\nQuery: '{q}' -> {len(results)} results")
    for res in results[:8]:
        p = res['product']
        print(f"  {res['score']:.3f}  {p['category']:<25}  {p['title'][:40]}")
    if len(results) > 8:
        print(f"  ... and {len(results)-8} more")
    print()
