import os
from pathlib import Path

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
    name: str
    category: str
    price: float
    stock: int
    available: bool

    description: str | None = None
    discount: float = Field(
        default=0.0,
        ge=0,
        le=100,
    )


# === Generate ===

prompt = """
Provide information about a laptop product.

Include:
- name
- category
- price
- stock
- available

Description and discount are optional.
If they are not provided, they should use their application defaults.

Return the information as structured data.
"""

print("\n=== OUTPUT SCHEMA ===")
print(Product.model_json_schema())

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

print("\n=== RAW MODEL RESPONSE ===")
print(response.text)


# === Parse and Validate ===

try:

    product = Product.model_validate_json(
        response.text
    )

    print("\n=== VALIDATED PRODUCT ===")
    print("[Valid]")
    print(product)

except ValidationError as error:

    print("\n=== VALIDATION ERROR ===")

    for item in error.errors():

        field = ".".join(
            str(value)
            for value in item["loc"]
        )

        print(
            f"- {field}: {item['msg']}"
        )

    product = None


# === Default Value Examples ===

default_examples = {
    "missing_optional_fields": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": 25,
        "available": True,
    },
    "explicit_optional_values": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": 25,
        "available": True,
        "description": "Business laptop",
        "discount": 10.0,
    },
    "explicit_null_description": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": 25,
        "available": True,
        "description": None,
    },
}


print("\n=== DEFAULT VALUE EXAMPLES ===")

for name, data in default_examples.items():

    print(f"\n--- {name} ---")

    try:

        example = Product.model_validate(data)

        print("[Valid]")
        print(example)

        print(
            f"[Description] {example.description}"
        )

        print(
            f"[Discount] {example.discount}"
        )

    except ValidationError as error:

        print("[Invalid]")

        for item in error.errors():

            field = ".".join(
                str(value)
                for value in item["loc"]
            )

            print(
                f"- {field}: {item['msg']}"
            )


# === Required Field Example ===

print("\n=== REQUIRED FIELD EXAMPLE ===")

missing_required_field = {
    "name": "ProBook 15",
    "category": "Laptop",
    "price": 1299.99,
    "stock": 25,
}


try:

    Product.model_validate(
        missing_required_field
    )

    print("[Valid]")

except ValidationError as error:

    print("[Invalid]")

    for item in error.errors():

        field = ".".join(
            str(value)
            for value in item["loc"]
        )

        print(
            f"- {field}: {item['msg']}"
        )


# === Application Values ===

print("\n=== APPLICATION VALUES ===")

if product is not None:

    print(f"[Name] {product.name}")
    print(f"[Category] {product.category}")
    print(f"[Price] {product.price}")
    print(f"[Stock] {product.stock}")
    print(f"[Available] {product.available}")
    print(f"[Description] {product.description}")
    print(f"[Discount] {product.discount}")
