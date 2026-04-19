"""Find available Gemini models and test generation."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from backend.config import GEMINI_API_KEY
from google import genai

client = genai.Client(api_key=GEMINI_API_KEY)

# List available models
results = []
for model in client.models.list():
    name = model.name
    if 'flash' in name.lower() or 'pro' in name.lower():
        results.append(name)

with open('models_list.txt', 'w') as f:
    for r in sorted(results):
        f.write(r + '\n')

print(f"Found {len(results)} models. Written to models_list.txt")

# Try generation with different model names
test_models = [
    "gemini-2.0-flash",
    "gemini-1.5-flash",
    "models/gemini-2.0-flash",
    "models/gemini-1.5-flash",
    "gemini-2.0-flash-lite",
]

for m in test_models:
    try:
        response = client.models.generate_content(
            model=m,
            contents="Say hello in one word."
        )
        print(f"  {m} -> OK: {response.text[:50]}")
        break
    except Exception as e:
        print(f"  {m} -> FAIL: {str(e)[:80]}")
