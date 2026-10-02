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


# === Exact Match Evaluators ===

def exact_match(actual: str, expected: str) -> bool:
    """Matches strings exactly, including case and whitespace."""

    return actual == expected


def case_insensitive_match(actual: str, expected: str) -> bool:
    """Matches strings while ignoring letter case."""

    return actual.lower() == expected.lower()


def normalized_match(actual: str, expected: str) -> bool:
    """Matches strings after normalizing whitespace."""

    actual_normalized = " ".join(actual.split())
    expected_normalized = " ".join(expected.split())

    return actual_normalized == expected_normalized


# === Evaluator Selection ===

evaluators = {
    "exact": exact_match,
    "case_insensitive": case_insensitive_match,
    "normalized": normalized_match,
}


# === Test Cases ===
#
# Add new test cases here without changing the execution loop.

test_cases = [
    {
        "name": "Arithmetic",
        "prompt": "What is 2 + 2? Reply with only the number.",
        "expected": "4",
        "match_type": "exact",
    },
    {
        "name": "Capital City",
        "prompt": "What is the capital of France? Reply with only the city name.",
        "expected": "Paris",
        "match_type": "case_insensitive",
    },
    {
        "name": "Sentence",
        "prompt": "Complete this sentence: The sky is blue. Reply with only the completed sentence.",
        "expected": "The sky is blue.",
        "match_type": "normalized",
    },
]


# === Run Evaluation ===

print("=== Exact Match Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    expected = test_case["expected"]
    match_type = test_case["match_type"]

    evaluator = evaluators[match_type]

    result = evaluator(actual, expected)

    print(f"[Match Type] {match_type}")
    print(f"[Expected]  {expected}")
    print(f"[Actual]    {actual}")

    if result:
        print("[Result]    PASS")
        passed += 1
    else:
        print("[Result]    FAIL")
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
