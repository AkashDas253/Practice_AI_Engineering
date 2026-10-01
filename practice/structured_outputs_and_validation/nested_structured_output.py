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


# === Nested Models ===

class Pricing(BaseModel):
    currency: str
    amount: float


class Supplier(BaseModel):
    name: str
    country: str


class Product(BaseModel):
    name: str
    category: str
    pricing: Pricing
    supplier: Supplier


print("\n=== OUTPUT SCHEMA ===")
print(Product.model_json_schema())


# === Request ===

prompt = """
Provide information about a laptop.

Include:
- name
- category
- pricing with currency and amount
- supplier with name and country

Return the information as structured data.
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Generate Structured Output ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": Product,
    },
)


# === Raw Response ===

print("\n=== RAW MODEL RESPONSE ===")
print(response.text)


# === Validate Nested Output ===

product = Product.model_validate_json(response.text)


# === Nested Object ===

print("\n=== VALIDATED PRODUCT ===")

print(f"[Name] {product.name}")
print(f"[Category] {product.category}")

print("\n[Pricing]")
print(f"Currency: {product.pricing.currency}")
print(f"Amount: {product.pricing.amount}")

print("\n[Supplier]")
print(f"Name: {product.supplier.name}")
print(f"Country: {product.supplier.country}")
