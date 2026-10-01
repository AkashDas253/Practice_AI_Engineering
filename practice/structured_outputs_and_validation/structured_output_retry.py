import os
import json
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

MAX_ATTEMPTS = 3


# === Model ===

class Product(BaseModel):
    name: str
    category: str
    price: float
    stock: int
    available: bool


# === Application Validation ===

def validate_product(data: dict) -> Product:

    product = Product.model_validate(data)

    if product.price <= 0:
        raise ValueError("Price must be greater than 0.")

    if product.stock < 0:
        raise ValueError("Stock must be greater than or equal to 0.")

    return product


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


def generate_product(instruction: str) -> str:

    response = client.models.generate_content(
        model=model,
        contents=instruction,
        config={
            "response_mime_type": "application/json",
            "response_schema": Product,
        },
    )

    return response.text


# === Retry ===

print("\n=== USER REQUEST ===")
print(prompt)

product = None

for attempt in range(1, MAX_ATTEMPTS + 1):

    print(f"\n=== ATTEMPT {attempt} ===")

    if attempt == 1:

        request = prompt

    else:

        request = f"""
{prompt}

The previous response did not pass application validation.

Return a complete product object.
Make sure all required fields are present.
Make sure price is greater than 0.
Make sure stock is greater than or equal to 0.
"""

    try:

        raw_response = generate_product(request)

        print("\n=== RAW MODEL RESPONSE ===")
        print(raw_response)

        data = json.loads(raw_response)

        product = validate_product(data)

        print("\n=== VALIDATION ===")
        print("[Valid]")

        print("\n=== RETRY STATUS ===")
        print(f"Validation succeeded on attempt {attempt}.")

        break

    except json.JSONDecodeError as error:

        print("\n=== VALIDATION ===")
        print("[Invalid JSON]")
        print(f"- {error}")

    except ValidationError as error:

        print("\n=== VALIDATION ===")
        print("[Invalid]")

        for item in error.errors():

            field = ".".join(
                str(value)
                for value in item["loc"]
            )

            print(
                f"- {field}: {item['msg']}"
            )

    except ValueError as error:

        print("\n=== VALIDATION ===")
        print("[Invalid]")
        print(f"- {error}")

    if attempt < MAX_ATTEMPTS:

        print("\n=== RETRY ===")
        print(
            f"Retrying... "
            f"{MAX_ATTEMPTS - attempt} attempt(s) remaining."
        )

    else:

        print("\n=== RETRY STATUS ===")
        print("Maximum retry attempts reached.")


# === Application Result ===

print("\n=== APPLICATION RESULT ===")

if product is not None:

    print("[Accepted]")
    print(product)

    print("\n[Application Values]")
    print(f"[Name] {product.name}")
    print(f"[Category] {product.category}")
    print(f"[Price] {product.price}")
    print(f"[Stock] {product.stock}")
    print(f"[Available] {product.available}")

else:

    print("[Rejected]")
    print("No validated structured output was produced.")
