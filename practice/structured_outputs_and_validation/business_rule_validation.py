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
    name: str = Field(
        min_length=3,
        max_length=50,
    )

    category: str

    price: float = Field(
        ge=0,
        le=10000,
    )

    stock: int = Field(
        ge=0,
        le=1000,
    )

    discount: float = Field(
        ge=0,
        le=100,
    )


print("\n=== OUTPUT SCHEMA ===")
print(Product.model_json_schema())


# === Request ===

prompt = """
Generate information about a laptop product.

Set the category to "Laptop".

Include:
- name
- category
- price
- stock
- discount

Return valid structured data.
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


# === Structural and Field Validation ===

print("\n=== STRUCTURAL AND FIELD VALIDATION ===")

try:

    product = Product.model_validate_json(response.text)

    print("[Valid]")
    print(product)

except ValidationError as error:

    print("[Invalid]")
    print(error)

    raise SystemExit


# === Business Rules ===

def validate_business_rules(product: Product) -> list[str]:
    """Validates application-specific business rules."""

    errors = []

    if product.category.lower() == "laptop" and product.price < 300:
        errors.append(
            "Laptops must have a price of at least 300."
        )

    if product.discount > 50:
        errors.append(
            "Discounts above 50 percent are not allowed."
        )

    if product.stock > 500 and product.discount > 30:
        errors.append(
            "Products with more than 500 units in stock "
            "cannot have a discount above 30 percent."
        )

    return errors


# === Business Rule Validation ===

print("\n=== BUSINESS RULE VALIDATION ===")

business_errors = validate_business_rules(product)

if business_errors:

    print("[Business Rules Failed]")

    for error in business_errors:
        print(f"- {error}")

else:

    print("[Business Rules Passed]")


# === Business Rule Examples ===

print("\n=== BUSINESS RULE EXAMPLES ===")


# === Valid Product ===

print("\n--- valid_product ---")

valid_product = Product(
    name="ProBook 15",
    category="Laptop",
    price=1299.99,
    stock=100,
    discount=20,
)

errors = validate_business_rules(valid_product)

if errors:

    print("[Business Rules Failed]")

    for error in errors:
        print(f"- {error}")

else:

    print("[Business Rules Passed]")


# === Laptop Below Minimum Price ===

print("\n--- laptop_below_minimum_price ---")

low_price_laptop = Product(
    name="Budget Laptop",
    category="Laptop",
    price=250,
    stock=100,
    discount=10,
)

errors = validate_business_rules(low_price_laptop)

if errors:

    print("[Business Rules Failed]")

    for error in errors:
        print(f"- {error}")

else:

    print("[Business Rules Passed]")


# === Excessive Discount ===

print("\n--- excessive_discount ---")

excessive_discount = Product(
    name="ProBook 15",
    category="Laptop",
    price=1299.99,
    stock=100,
    discount=60,
)

errors = validate_business_rules(excessive_discount)

if errors:

    print("[Business Rules Failed]")

    for error in errors:
        print(f"- {error}")

else:

    print("[Business Rules Passed]")


# === High Stock With High Discount ===

print("\n--- high_stock_high_discount ---")

high_stock_discount = Product(
    name="ProBook 15",
    category="Laptop",
    price=1299.99,
    stock=750,
    discount=40,
)

errors = validate_business_rules(high_stock_discount)

if errors:

    print("[Business Rules Failed]")

    for error in errors:
        print(f"- {error}")

else:

    print("[Business Rules Passed]")
