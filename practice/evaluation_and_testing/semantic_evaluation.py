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


# === Semantic Evaluation ===

def evaluate_semantically(
    actual: str,
    expected: str,
) -> tuple[bool, str]:
    """Uses the model to determine whether two answers have the same meaning."""

    judge_prompt = f"""
You are evaluating whether two answers have the same meaning.

Expected answer:
{expected}

Actual answer:
{actual}

Determine whether the actual answer is semantically aligned
with the expected answer.

Ignore differences in wording, sentence structure, and style.

Reply using exactly this format:

PASS: <short reason>

or

FAIL: <short reason>
"""

    judgment = call_model(judge_prompt)

    first_line = judgment.splitlines()[0].strip()

    if first_line.upper().startswith("PASS:"):
        return True, first_line[5:].strip()

    if first_line.upper().startswith("FAIL:"):
        return False, first_line[5:].strip()

    return False, f"Unrecognized evaluator response: {judgment}"


# === Test Cases ===
#
# Add new test cases here without changing the execution loop.

test_cases = [
    {
        "name": "Equivalent Meaning",
        "prompt": "What is the capital of France? Answer in a complete sentence.",
        "expected": "Paris is the capital city of France.",
    },
    {
        "name": "Different Wording",
        "prompt": "Explain what Python is.",
        "expected": "Python is a programming language.",
    },
    {
        "name": "Different Meaning",
        "prompt": "What is the capital of Germany?",
        "expected": "Paris is the capital city of France.",
    },
]


# === Run Evaluation ===

print("=== Semantic Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    expected = test_case["expected"]

    result, reason = evaluate_semantically(
        actual,
        expected,
    )

    print(f"[Expected] {expected}")
    print(f"[Actual]   {actual}")
    print(f"[Reason]   {reason}")

    if result:
        print("[Result]   PASS")
        passed += 1
    else:
        print("[Result]   FAIL")
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
