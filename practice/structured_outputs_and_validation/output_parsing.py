import json


# === Sample Model Outputs ===

valid_output = """
{
    "name": "UltraBook Pro 15",
    "category": "Laptop",
    "price": 1299.99,
    "available": true
}
"""

malformed_output = """
{
    "name": "UltraBook Pro 15",
    "category": "Laptop",
    "price": 1299.99,
    "available": true
"""

unexpected_structure_output = """
[
    {
        "name": "UltraBook Pro 15",
        "category": "Laptop"
    }
]
"""

incomplete_output = """
{
    "name": "UltraBook Pro 15",
    "category": "Laptop"
}
"""

extra_fields_output = """
{
    "name": "UltraBook Pro 15",
    "category": "Laptop",
    "price": 1299.99,
    "available": true,
    "color": "Silver"
}
"""


# === Parsing ===

def parse_json_output(raw_output: str) -> object:
    """Parses raw JSON output."""

    return json.loads(raw_output)


def require_object(parsed_output: object) -> dict:
    """Requires the parsed JSON value to be an object."""

    if not isinstance(parsed_output, dict):
        raise TypeError("Expected a JSON object.")

    return parsed_output


# === Valid JSON ===

print("\n=== VALID JSON ===")

try:

    parsed_output = parse_json_output(valid_output)

    print("[Raw Type]")
    print(type(parsed_output).__name__)

    parsed_output = require_object(parsed_output)

    print("[Parsed]")
    print(parsed_output)

except (json.JSONDecodeError, TypeError) as error:

    print("[Parsing Error]")
    print(error)


# === Malformed JSON ===

print("\n=== MALFORMED JSON ===")

try:

    parsed_output = parse_json_output(
        malformed_output
    )

    print("[Parsed]")
    print(parsed_output)

except json.JSONDecodeError as error:

    print("[Parsing Error]")
    print(error)


# === Unexpected Top-Level Structure ===

print("\n=== UNEXPECTED TOP-LEVEL STRUCTURE ===")

try:

    parsed_output = parse_json_output(
        unexpected_structure_output
    )

    print("[Raw Type]")
    print(type(parsed_output).__name__)

    parsed_output = require_object(parsed_output)

    print("[Parsed]")
    print(parsed_output)

except (json.JSONDecodeError, TypeError) as error:

    print("[Parsing Error]")
    print(error)


# === Incomplete Object ===

print("\n=== INCOMPLETE OBJECT ===")

try:

    parsed_output = parse_json_output(
        incomplete_output
    )

    parsed_output = require_object(parsed_output)

    print("[Parsed]")
    print(parsed_output)

    print(
        "[Status] Parsing succeeded; "
        "field validation has not been performed."
    )

except (json.JSONDecodeError, TypeError) as error:

    print("[Parsing Error]")
    print(error)


# === Extra Fields ===

print("\n=== EXTRA FIELDS ===")

try:

    parsed_output = parse_json_output(
        extra_fields_output
    )

    parsed_output = require_object(parsed_output)

    print("[Parsed]")
    print(parsed_output)

    print(
        "[Status] Parsing succeeded; "
        "extra-field validation has not been performed."
    )

except (json.JSONDecodeError, TypeError) as error:

    print("[Parsing Error]")
    print(error)


# === Application Values ===

print("\n=== APPLICATION VALUES ===")

try:

    parsed_output = parse_json_output(
        valid_output
    )

    parsed_output = require_object(parsed_output)

    print(f"[Name] {parsed_output.get('name')}")
    print(f"[Category] {parsed_output.get('category')}")
    print(f"[Price] {parsed_output.get('price')}")
    print(f"[Available] {parsed_output.get('available')}")

except (json.JSONDecodeError, TypeError) as error:

    print("[Application Error]")
    print(error)
