"""Direct test of Gemini API to diagnose generator issues."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from backend.config import GEMINI_API_KEY
from google import genai
from google.genai import types

print(f"API Key present: {bool(GEMINI_API_KEY)}")
print(f"API Key (first 10 chars): {GEMINI_API_KEY[:10]}...")

client = genai.Client(api_key=GEMINI_API_KEY)

# Test 1: Simple text generation
print("\n--- Test 1: Simple text generation ---")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Hello, what is 2+2?"
    )
    print(f"  Response type: {type(response)}")
    print(f"  Has .text: {hasattr(response, 'text')}")
    print(f"  Text: {response.text[:200]}")
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

# Test 2: With types.Content
print("\n--- Test 2: With types.Content ---")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=[types.Content(parts=[types.Part.from_text(text="What color is the sky?")])]
    )
    print(f"  Response type: {type(response)}")
    print(f"  Has .text: {hasattr(response, 'text')}")
    if hasattr(response, 'text') and response.text:
        print(f"  Text: {response.text[:200]}")
    elif response.candidates:
        print(f"  Candidate text: {response.candidates[0].content.parts[0].text[:200]}")
    else:
        print(f"  No text found in response")
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

# Test 3: Simple string contents (the way it originally worked)
print("\n--- Test 3: Simple string contents ---")
try:
    response = client.models.generate_content(
        model="gemini-1.5-flash",
        contents="Recommend the Sony WH-1000XM5 headphones in 2 sentences."
    )
    print(f"  Text: {response.text[:300]}")
except Exception as e:
    print(f"  ERROR: {type(e).__name__}: {e}")

print("\n--- Tests complete ---")
