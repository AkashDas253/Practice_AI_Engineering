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


# === Schema ===

product_schema = {
    "type": "object",
    "properties": {
        "product_name": {
            "type": "string",
            "description": "Name of the product.",
        },
        "category": {
            "type": "string",
            "description": "Product category.",
        },
        "price": {
            "type": "number",
            "description": "Product price.",
        },
        "available": {
            "type": "boolean",
            "description": "Whether the product is currently available.",
        },
    },
    "required": [
        "product_name",
        "category",
        "price",
        "available",
    ],
}


print("\n=== OUTPUT SCHEMA ===")
print(product_schema)


# === Request ===

prompt = """
Provide information about a laptop.

Return:
- product name
- category
- price
- availability
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Structured Output ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=product_schema,
    ),
)


# === Result ===

print("\n=== STRUCTURED RESPONSE ===")
print(response.text)
