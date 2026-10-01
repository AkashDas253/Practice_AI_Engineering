import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Pydantic Model ===

class Product(BaseModel):
    product_name: str
    category: str
    price: float
    available: bool


print("\n=== PYDANTIC MODEL ===")
print(Product.model_json_schema())


# === Request ===

prompt = """
Provide information about a laptop.

Include:
- product name
- category
- price
- availability
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Generate Structured Output ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=Product,
    ),
)


# === Raw Response ===

print("\n=== RAW MODEL RESPONSE ===")
print(response.text)


# === Parse Into Pydantic Model ===

product = Product.model_validate_json(response.text)


# === Typed Application Object ===

print("\n=== PYDANTIC OBJECT ===")
print(product)

print("\n=== APPLICATION VALUES ===")
print(f"[Product] {product.product_name}")
print(f"[Category] {product.category}")
print(f"[Price] {product.price}")
print(f"[Available] {product.available}")
