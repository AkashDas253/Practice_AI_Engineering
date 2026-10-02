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

def evaluate_response(
    actual: str,
    expected: str,
) -> bool:
    """Checks whether the response matches the expected answer."""

    return actual.strip().lower() == expected.strip().lower()


# === Test Dataset ===
#
# Add new test cases here without changing the evaluation loop.

test_cases = [
    {
        "name": "Simple Arithmetic",
        "prompt": "What is 2 + 2? Reply with only the answer.",
        "expected": "4",
    },
    {
        "name": "Capital City",
        "prompt": "What is the capital of France? Reply with only the city name.",
        "expected": "Paris",
    },
    {
        "name": "Programming Language",
        "prompt": "Is Python a programming language? Reply with only Yes or No.",
        "expected": "Yes",
    },
]


# === Batch Evaluation ===

print("=== Batch Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

results = []

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    expected = test_case["expected"]

    passed = evaluate_response(
        actual,
        expected,
    )

    result = {
        "name": test_case["name"],
        "expected": expected,
        "actual": actual,
        "passed": passed,
    }

    results.append(result)

    print(f"[Expected] {expected}")
    print(f"[Actual]   {actual}")

    if passed:
        print("[Result]   PASS")
    else:
        print("[Result]   FAIL")


# === Aggregate Results ===

total = len(results)

passed_count = sum(
    result["passed"]
    for result in results
)

failed_count = total - passed_count


# === Summary ===

print("\n=== Batch Evaluation Summary ===")
print(f"Total:  {total}")
print(f"Passed: {passed_count}")
print(f"Failed: {failed_count}")

if total > 0:
    pass_rate = (passed_count / total) * 100
else:
    pass_rate = 0.0

print(f"Pass Rate: {pass_rate:.2f}%")

if failed_count == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
