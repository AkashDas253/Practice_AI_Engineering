import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from pydantic import BaseModel, Field, ValidationError


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Output Schema ===

class ProductReview(BaseModel):
    product: str
    rating: int = Field(ge=1, le=5)
    summary: str
    sentiment: str


# === Model Call ===

def call_model(prompt: str) -> str:
    """Sends a prompt to the model and returns the response text."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text.strip()


# === JSON Cleanup ===

def clean_json_response(response_text: str) -> str:
    """Removes common Markdown code fences around JSON."""

    cleaned = response_text.strip()

    if cleaned.startswith("```json"):
        cleaned = cleaned[len("```json"):].strip()

    elif cleaned.startswith("```"):
        cleaned = cleaned[len("```"):].strip()

    if cleaned.endswith("```"):
        cleaned = cleaned[:-3].strip()

    return cleaned


# === Schema Evaluation ===

def validate_schema(
    response_text: str,
) -> tuple[bool, ProductReview | None, str]:
    """Parses and validates model output against the ProductReview schema."""

    try:
        cleaned = clean_json_response(response_text)

        data = json.loads(cleaned)

        result = ProductReview.model_validate(data)

        return True, result, ""

    except json.JSONDecodeError as error:
        return False, None, f"Invalid JSON: {error}"

    except ValidationError as error:
        return False, None, f"Schema validation failed: {error}"


# === Additional Validation Rules ===

def validate_business_rules(
    review: ProductReview,
) -> tuple[bool, list[str]]:
    """Checks rules beyond basic Pydantic field validation."""

    errors = []

    if not review.product.strip():
        errors.append("product must not be empty")

    if not review.summary.strip():
        errors.append("summary must not be empty")

    if not review.sentiment.strip():
        errors.append("sentiment must not be empty")

    allowed_sentiments = {
        "positive",
        "negative",
        "neutral",
    }

    if review.sentiment.lower() not in allowed_sentiments:
        errors.append(
            "sentiment must be one of: "
            "positive, negative, neutral"
        )

    return len(errors) == 0, errors


# === Test Cases ===
#
# Each test checks whether the model produces data that satisfies
# the required schema and validation rules.

test_cases = [
    {
        "name": "Positive Review",
        "prompt": """
        Create a product review for wireless headphones.
        Return JSON with these fields:
        product, rating, summary, sentiment.

        Rules:
        - rating must be an integer from 1 to 5.
        - sentiment must describe the review sentiment.
        - Keep the summary short.
        """,
    },
    {
        "name": "Negative Review",
        "prompt": """
        Create a negative product review for a laptop.
        Return JSON with these fields:
        product, rating, summary, sentiment.

        Rules:
        - rating must be an integer from 1 to 5.
        - sentiment must describe the review sentiment.
        - Keep the summary short.
        """,
    },
    {
        "name": "Neutral Review",
        "prompt": """
        Create a neutral product review for a smartphone.
        Return JSON with these fields:
        product, rating, summary, sentiment.

        Rules:
        - rating must be an integer from 1 to 5.
        - sentiment must describe the review sentiment.
        - Keep the summary short.
        """,
    },
]


# === Run Evaluation ===

print("=== Structured Output Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])

    print("[Raw Output]")
    print(actual)

    schema_valid, review, schema_error = validate_schema(actual)

    if not schema_valid:
        print("[Schema]  FAIL")
        print(f"[Reason]  {schema_error}")
        print("[Result]  FAIL")

        failed += 1
        continue

    print("[Schema]  PASS")

    rules_valid, rule_errors = validate_business_rules(review)

    if rules_valid:
        print("[Rules]   PASS")
        print("[Result]  PASS")
        passed += 1

    else:
        print("[Rules]   FAIL")

        for error in rule_errors:
            print(f"[Reason]  {error}")

        print("[Result]  FAIL")
        failed += 1


# === Summary ===

total = len(test_cases)

print("\n=== Evaluation Summary ===")
print(f"Total:  {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
