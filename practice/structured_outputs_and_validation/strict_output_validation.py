import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from pydantic import BaseModel, Field, ValidationError


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Application Model ===

class Product(BaseModel):
    name: str = Field(min_length=3)
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    available: bool


# === Model Output Schema ===

response_schema = {
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
        },
        "category": {
            "type": "string",
        },
        "price": {
            "type": "number",
        },
        "stock": {
            "type": "integer",
        },
        "available": {
            "type": "boolean",
        },
    },
    "required": [
        "name",
        "category",
        "price",
        "stock",
        "available",
    ],
}


print("\n=== OUTPUT SCHEMA ===")
print(response_schema)


# === User Request ===

prompt = """
Provide information about a laptop product.

Include:
- name
- category
- price
- stock
- available

Return the information as structured data.
"""

print("\n=== USER REQUEST ===")
print(prompt)


# === Model Response ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config=types.GenerateContentConfig(
        response_mime_type="application/json",
        response_schema=response_schema,
    ),
)

raw_output = response.text

print("\n=== RAW MODEL RESPONSE ===")
print(raw_output)


# === Strict Validation ===

print("\n=== STRICT VALIDATION ===")

try:

    product = Product.model_validate_json(
        raw_output,
        strict=True,
    )

    print("[Accepted]")
    print(product)

except ValidationError as error:

    print("[Rejected]")

    for issue in error.errors():

        field = ".".join(
            str(part)
            for part in issue["loc"]
        )

        print(
            f"- {field}: {issue['msg']}"
        )

    product = None


# === Application Decision ===

print("\n=== APPLICATION DECISION ===")

if product is None:

    print(
        "[Fail Closed] Product was rejected because "
        "it did not completely satisfy the required contract."
    )

else:

    print("[Accepted] Product is safe to use.")

    print(f"[Name] {product.name}")
    print(f"[Category] {product.category}")
    print(f"[Price] {product.price}")
    print(f"[Stock] {product.stock}")
    print(f"[Available] {product.available}")


# === Strict Validation Examples ===

print("\n=== STRICT VALIDATION EXAMPLES ===")


examples = {
    "complete_product": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": 25,
        "available": True,
    },
    "missing_stock": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "available": True,
    },
    "invalid_price": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": -100,
        "stock": 25,
        "available": True,
    },
    "invalid_type": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": "many",
        "available": True,
    },
}


for name, data in examples.items():

    print(f"\n--- {name} ---")

    try:

        product = Product.model_validate(
            data,
            strict=True,
        )

        print("[Accepted]")
        print(product)

    except ValidationError as error:

        print("[Rejected]")

        for issue in error.errors():

            field = ".".join(
                str(part)
                for part in issue["loc"]
            )

            print(
                f"- {field}: {issue['msg']}"
            )
