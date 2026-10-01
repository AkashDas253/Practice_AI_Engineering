import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError


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
    name: str = Field(
        min_length=3,
        max_length=50,
    )

    category: Literal[
        "Laptop",
        "Tablet",
        "Phone",
    ]

    price: float = Field(
        ge=0,
        le=10000,
    )

    stock: int = Field(
        ge=0,
        le=1000,
    )

    product_code: str = Field(
        min_length=5,
        max_length=12,
        pattern=r"^[A-Z]{3}-[0-9]{2,8}$",
    )


print("\n=== OUTPUT SCHEMA ===")
print(Product.model_json_schema())


# === Request ===

prompt = """
Generate information about a laptop product.

Include:
- name
- category
- price
- stock
- product_code

Follow these requirements:
- name must be between 3 and 50 characters
- category must be Laptop, Tablet, or Phone
- price must be between 0 and 10000
- stock must be between 0 and 1000
- product_code must follow the format ABC-123
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


# === Model Validation ===

print("\n=== MODEL OUTPUT VALIDATION ===")

try:

    product = Product.model_validate_json(response.text)

    print("[Valid]")
    print(product)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Field Constraint Examples ===

print("\n=== FIELD CONSTRAINT EXAMPLES ===")


# === Valid Product ===

print("\n--- valid_product ---")

valid_product = {
    "name": "ProBook 15",
    "category": "Laptop",
    "price": 1299.99,
    "stock": 25,
    "product_code": "LAP-123",
}

try:

    product = Product.model_validate(valid_product)

    print("[Valid]")
    print(product)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Invalid Enum ===

print("\n--- invalid_category ---")

invalid_category = {
    "name": "ProBook 15",
    "category": "Computer",
    "price": 1299.99,
    "stock": 25,
    "product_code": "LAP-123",
}

try:

    Product.model_validate(invalid_category)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Invalid Numeric Range ===

print("\n--- invalid_price ---")

invalid_price = {
    "name": "ProBook 15",
    "category": "Laptop",
    "price": 15000,
    "stock": 25,
    "product_code": "LAP-123",
}

try:

    Product.model_validate(invalid_price)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Invalid String Length ===

print("\n--- invalid_name ---")

invalid_name = {
    "name": "PC",
    "category": "Laptop",
    "price": 1299.99,
    "stock": 25,
    "product_code": "LAP-123",
}

try:

    Product.model_validate(invalid_name)

except ValidationError as error:

    print("[Invalid]")
    print(error)


# === Invalid Pattern ===

print("\n--- invalid_product_code ---")

invalid_product_code = {
    "name": "ProBook 15",
    "category": "Laptop",
    "price": 1299.99,
    "stock": 25,
    "product_code": "laptop-123",
}

try:

    Product.model_validate(invalid_product_code)

except ValidationError as error:

    print("[Invalid]")
    print(error)
