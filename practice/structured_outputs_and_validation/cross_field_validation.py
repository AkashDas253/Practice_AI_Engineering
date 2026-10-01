import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError, model_validator


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
    price: float
    stock: int
    available: bool

    @model_validator(mode="after")
    def validate_inventory_state(self):
        """Validates relationships between inventory fields."""

        if self.available and self.stock == 0:
            raise ValueError(
                "A product cannot be available when stock is zero."
            )

        if not self.available and self.stock > 0:
            raise ValueError(
                "A product marked unavailable cannot have positive stock."
            )

        return self


print("\n=== OUTPUT SCHEMA ===")
print(Product.model_json_schema())


# === Request ===

prompt = """
Generate information about a laptop product.

Include:
- name
- price
- stock
- available

The product should represent a valid inventory state.
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


# === Validate Model Output ===

print("\n=== MODEL OUTPUT VALIDATION ===")

try:

    product = Product.model_validate_json(response.text)

    print("[Valid]")
    print(product)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Cross-Field Validation Examples ===

print("\n=== CROSS-FIELD VALIDATION EXAMPLES ===")


# === Valid Inventory ===

print("\n--- valid_inventory ---")

valid_inventory = {
    "name": "ProBook 15",
    "price": 1299.99,
    "stock": 10,
    "available": True,
}

try:

    product = Product.model_validate(valid_inventory)

    print("[Valid]")
    print(product)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Available Without Stock ===

print("\n--- available_without_stock ---")

available_without_stock = {
    "name": "ProBook 15",
    "price": 1299.99,
    "stock": 0,
    "available": True,
}

try:

    Product.model_validate(available_without_stock)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Unavailable With Stock ===

print("\n--- unavailable_with_stock ---")

unavailable_with_stock = {
    "name": "ProBook 15",
    "price": 1299.99,
    "stock": 10,
    "available": False,
}

try:

    Product.model_validate(unavailable_with_stock)

except ValidationError as error:

    print("[Invalid]")
    print(error)
