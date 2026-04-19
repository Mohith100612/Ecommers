import requests
import json

r = requests.post('http://localhost:8000/search', params={'query_text': 'Sony noise cancelling headphones', 'top_k': 3})
data = r.json()

print(f"HTTP Status: {r.status_code}")
print(f"Results count: {len(data.get('results', []))}")
print()

for i, res in enumerate(data.get('results', [])):
    p = res['product']
    print(f"Result {i+1}: {p['title']} | ${p['price']} | Score: {res['score']:.3f}")

print()
print("=" * 50)
print("AI ASSISTANT ANSWER:")
print("=" * 50)
print(data.get('answer', 'NO ANSWER'))
