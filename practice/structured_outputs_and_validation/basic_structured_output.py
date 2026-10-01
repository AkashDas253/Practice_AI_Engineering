import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Request ===

prompt = """
Return information about a laptop as structured data.

Include:
- product name
- category
- price
- available
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Structured Output ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
    ),
)


# === Result ===

print("\n=== STRUCTURED RESPONSE ===")
print(response.text)
