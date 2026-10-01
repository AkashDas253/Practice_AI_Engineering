import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError, Field


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
    name: str = Field(min_length=3)
    category: str
    price: float
    stock: int = Field(ge=0)
    available: bool


# === Request ===

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


# === Generate ===

response = client.models.generate_content(
    model=model,
    contents=prompt,
    config={
        "response_mime_type": "application/json",
        "response_schema": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "category": {"type": "string"},
                "price": {"type": "number"},
                "stock": {"type": "integer"},
                "available": {"type": "boolean"},
            },
            "required": [
                "name",
                "category",
                "price",
                "stock",
                "available",
            ],
        },
    },
)


# === Raw Output ===

print("\n=== RAW MODEL RESPONSE ===")
print(response.text)


# === Parse ===

print("\n=== PARSE ===")

try:

    data = json.loads(response.text)

    print("[Parsed]")
    print(data)

except json.JSONDecodeError as error:

    print("[Parsing Failed]")
    print(error)

    data = None


# === Validate ===

product = None

if data is not None:

    print("\n=== VALIDATE ===")

    try:

        product = Product.model_validate(data)

        print("[Valid]")
        print(product)

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


# === Recover or Reject ===

print("\n=== RECOVER OR REJECT ===")

if product is not None:

    print("[Accepted]")
    print("Validated structured data is ready for application use.")

else:

    print("[Rejected]")
    print("Structured data did not pass validation.")


# === Application Use ===

print("\n=== APPLICATION USE ===")

if product is not None:

    print(f"[Name] {product.name}")
    print(f"[Category] {product.category}")
    print(f"[Price] {product.price}")
    print(f"[Stock] {product.stock}")
    print(f"[Available] {product.available}")

else:

    print("[Skipped]")
    print("No validated product is available.")


# === Pipeline Status ===

print("\n=== PIPELINE STATUS ===")

if product is not None:

    print(
        "[Success] "
        "Generate → Parse → Validate → Accept → Use"
    )

else:

    print(
        "[Rejected] "
        "Generate → Parse → Validate → Reject"
    )
