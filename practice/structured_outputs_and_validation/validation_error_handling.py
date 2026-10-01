from pydantic import BaseModel, Field, ValidationError


# === Model ===

class Product(BaseModel):
    name: str = Field(min_length=3)
    category: str
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    available: bool


# === Validation Helper ===

def validate_product(data: dict) -> Product | None:
    """Validates product data without crashing the application."""

    try:

        return Product.model_validate(data)

    except ValidationError as error:

        print("[Validation Failed]")

        for issue in error.errors():

            field = ".".join(
                str(part)
                for part in issue["loc"]
            )

            print(
                f"- {field}: {issue['msg']}"
            )

        return None


# === Valid Output ===

print("\n=== VALID OUTPUT ===")

valid_output = {
    "name": "UltraBook Pro 15",
    "category": "Laptop",
    "price": 1299.99,
    "stock": 45,
    "available": True,
}

product = validate_product(valid_output)

if product is not None:

    print("[Valid]")
    print(product)


# === Missing Required Field ===

print("\n=== MISSING REQUIRED FIELD ===")

missing_field_output = {
    "name": "UltraBook Pro 15",
    "category": "Laptop",
    "price": 1299.99,
    "available": True,
}

product = validate_product(missing_field_output)

if product is None:

    print("[Handled] Invalid output was rejected safely.")


# === Invalid Field Value ===

print("\n=== INVALID FIELD VALUE ===")

invalid_value_output = {
    "name": "PC",
    "category": "Laptop",
    "price": -100,
    "stock": 45,
    "available": True,
}

product = validate_product(invalid_value_output)

if product is None:

    print("[Handled] Invalid output was rejected safely.")


# === Multiple Validation Errors ===

print("\n=== MULTIPLE VALIDATION ERRORS ===")

multiple_errors_output = {
    "name": "PC",
    "category": "Laptop",
    "price": -100,
    "stock": -5,
    "available": "yes",
}

product = validate_product(multiple_errors_output)

if product is None:

    print("[Handled] Multiple validation errors were reported.")


# === Application Continues ===

print("\n=== APPLICATION CONTINUES ===")

products = [
    valid_output,
    missing_field_output,
    invalid_value_output,
]

valid_products = []

for data in products:

    product = validate_product(data)

    if product is not None:

        valid_products.append(product)


print(
    f"[Valid Products] {len(valid_products)}"
)

print(
    "[Status] Application continued after invalid outputs."
)
