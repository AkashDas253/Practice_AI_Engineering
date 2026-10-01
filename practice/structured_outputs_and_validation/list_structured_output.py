import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Models ===

class Product(BaseModel):
    name: str
    category: str
    price: float


class ProductList(BaseModel):
    products: list[Product]


print("\n=== OUTPUT SCHEMA ===")
print(ProductList.model_json_schema())


# === Request ===

prompt = """
Return information about three different laptop products.

For each product include:
- name
- category
- price

Return all products as a structured list.
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Generate Structured Output ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": ProductList,
    },
)


# === Raw Response ===

print("\n=== RAW MODEL RESPONSE ===")
print(response.text)


# === Validate Collection ===

product_list = ProductList.model_validate_json(response.text)


# === Validated Collection ===

print("\n=== VALIDATED PRODUCTS ===")

print(f"[Count] {len(product_list.products)}")

for index, product in enumerate(product_list.products, start=1):

    print(f"\n--- Product {index} ---")
    print(f"[Name] {product.name}")
    print(f"[Category] {product.category}")
    print(f"[Price] {product.price}")
