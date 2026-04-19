import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

def list_gemini_models():
    key = os.getenv("GEMINI_API_KEY")
    print(f"Testing Gemini Key: {key[:5]}...{key[-5:] if key else ''}")
    try:
        genai.configure(api_key=key)
        print("Accessible models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"- {m.name}")
        print("✅ Gemini: OK")
    except Exception as e:
        print(f"❌ Gemini Error: {e}")

if __name__ == "__main__":
    list_gemini_models()
