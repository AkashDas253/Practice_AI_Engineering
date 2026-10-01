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


# === Generate Structured Output ===

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


# === Complete Output ===

print("\n=== COMPLETE OUTPUT ===")

try:

    product_data = json.loads(response.text)

    product = Product.model_validate(product_data)

    print("[Valid]")
    print(product)

except (json.JSONDecodeError, ValidationError) as error:

    print("[Invalid]")
    print(error)


# === Partial Outputs ===

partial_outputs = {
    "missing_stock": {
        "name": "ProBook 15",
        "category": "Laptop",
        "price": 1299.99,
        "available": True,
    },
    "missing_multiple_fields": {
        "name": "ProBook 15",
        "category": "Laptop",
    },
    "empty_object": {},
}


print("\n=== PARTIAL OUTPUT EXAMPLES ===")

for name, data in partial_outputs.items():

    print(f"\n--- {name} ---")

    try:

        product = Product.model_validate(data)

        print("[Accepted]")
        print(product)

    except ValidationError as error:

        print("[Rejected]")

        for item in error.errors():

            field = ".".join(str(value) for value in item["loc"])

            print(
                f"- {field}: {item['msg']}"
            )


# === Application Handling ===

print("\n=== APPLICATION HANDLING ===")

candidate = {
    "name": "ProBook 15",
    "category": "Laptop",
    "price": 1299.99,
}

try:

    product = Product.model_validate(candidate)

    print("[Use]")
    print(product)

except ValidationError:

    print("[Not Used]")
    print("Incomplete structured output was rejected before reaching the application.")


print("\n=== STATUS ===")
print("Partial structured data is not treated as a valid Product.")
