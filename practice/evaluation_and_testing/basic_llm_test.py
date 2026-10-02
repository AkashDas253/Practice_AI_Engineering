import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Model Call ===

def call_model(prompt: str) -> str:
    """Sends a prompt to the model and returns the response text."""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text.strip()


# === Evaluation ===

def evaluate_response(actual: str, expected: str) -> bool:
    """Checks whether the actual response matches the expected response."""

    return actual.strip().lower() == expected.strip().lower()


# === Test Cases ===
#
# Add new test cases here without changing the execution loop.

test_cases = [
    {
        "name": "Simple arithmetic",
        "prompt": "What is 2 + 2? Reply with only the answer.",
        "expected": "4",
    },
    {
        "name": "Capital city",
        "prompt": "What is the capital of France? Reply with only the city name.",
        "expected": "Paris",
    },
    {
        "name": "Simple classification",
        "prompt": "Is Python a programming language? Reply with only Yes or No.",
        "expected": "Yes",
    },
]


# === Run Tests ===

print("=== Basic LLM Test ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    expected = test_case["expected"]

    print(f"[Expected] {expected}")
    print(f"[Actual]   {actual}")

    if evaluate_response(actual, expected):
        print("[Result]   PASS")
        passed += 1
    else:
        print("[Result]   FAIL")
        failed += 1


# === Summary ===

total = len(test_cases)

print("\n=== Test Summary ===")
print(f"Total:  {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
