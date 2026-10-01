import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, ValidationError


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


# === Generate ===

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


# === Parse ===

try:

    data = json.loads(response.text)

    print("\n=== PARSED OUTPUT ===")
    print(data)

except json.JSONDecodeError as error:

    print("\n=== PARSING ===")
    print("[Failed]")
    print(error)

    data = None


# === Validate ===

product = None

if data is not None:

    print("\n=== INITIAL VALIDATION ===")

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


# === Repair Examples ===

repair_examples = {
    "missing_category": {
        "name": "ProBook 15",
        "price": 1299.99,
        "stock": 25,
        "available": True,
    },
    "string_price": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": "1299.99",
        "stock": 25,
        "available": True,
    },
    "string_stock": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "stock": "25",
        "available": True,
    },
}


print("\n=== REPAIR EXAMPLES ===")

for name, original_data in repair_examples.items():

    print(f"\n--- {name} ---")

    print("[Original]")
    print(original_data)

    repaired_data = dict(original_data)

    if name == "missing_category":

        repaired_data["category"] = "Laptop"

    elif name == "string_price":

        repaired_data["price"] = float(
            repaired_data["price"]
        )

    elif name == "string_stock":

        repaired_data["stock"] = int(
            repaired_data["stock"]
        )

    print("[Repaired]")
    print(repaired_data)

    try:

        repaired_product = Product.model_validate(
            repaired_data
        )

        print("[Re-validation]")
        print("[Valid]")
        print(repaired_product)

    except (ValidationError, ValueError) as error:

        print("[Re-validation]")
        print("[Invalid]")
        print(error)


# === Application Result ===

print("\n=== APPLICATION RESULT ===")

if product is not None:

    print("[Accepted]")
    print(product)

else:

    print("[No Valid Original Output]")

print("\n[Status]")
print(
    "Repaired data must pass validation before it can be used."
)
