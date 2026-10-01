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


# === Model ===

class Product(BaseModel):
    name: str
    category: str
    description: str | None = None
    discount: float | None = None


print("\n=== MODEL SCHEMA ===")
print(Product.model_json_schema())


# === Generated Output ===

prompt = """
Provide information about a laptop.

Required:
- name
- category

Optional:
- description
- discount

If you do not have a description or discount, omit those fields.
"""

print("\n=== USER REQUEST ===")
print(prompt)


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


# === Validate Generated Output ===

product = Product.model_validate_json(response.text)


# === Validated Object ===

print("\n=== VALIDATED PRODUCT ===")

print(f"[Name] {product.name}")
print(f"[Category] {product.category}")
print(f"[Description] {product.description}")
print(f"[Discount] {product.discount}")


# === Missing Optional Fields ===

print("\n=== MISSING OPTIONAL FIELDS ===")

missing_optional = {
    "name": "Laptop A",
    "category": "Laptops",
}

product = Product.model_validate(missing_optional)

print("[Valid]")
print(product)


# === Nullable Fields ===

print("\n=== NULLABLE FIELDS ===")

nullable_fields = {
    "name": "Laptop B",
    "category": "Laptops",
    "description": None,
    "discount": None,
}

product = Product.model_validate(nullable_fields)

print("[Valid]")
print(product)


# === Missing Required Field ===

print("\n=== MISSING REQUIRED FIELD ===")

missing_required = {
    "name": "Laptop C",
}

try:

    Product.model_validate(missing_required)

except Exception as error:

    print("[Validation Error]")
    print(error)
