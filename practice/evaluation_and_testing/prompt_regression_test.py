import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Model Call ===

def call_model(prompt: str) -> tuple[str, str | None]:
    """Calls the model and returns response text and error."""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text.strip(), None

    except Exception as error:
        return "", str(error)


# === Evaluation ===

def evaluate_response(
    response: str,
    error: str | None,
    expected: str,
) -> bool:
    """Checks whether the response contains the expected answer."""

    if error is not None:
        return False

    return expected.lower() in response.lower()


# === Regression Test Cases ===
#
# These are cases that should continue passing
# after a prompt change.

test_cases = [
    {
        "name": "Simple Arithmetic",
        "input": "What is 2 + 2?",
        "expected": "4",
    },
    {
        "name": "Capital City",
        "input": "What is the capital of France?",
        "expected": "Paris",
    },
    {
        "name": "Programming Language",
        "input": "Is Python a programming language?",
        "expected": "Yes",
    },
]


# === Prompt Versions ===

baseline_prompt = """
Answer the user's question clearly and directly.

User question:
{input}
"""

changed_prompt = """
Answer the user's question.

Be extremely concise.
Return only the final answer.
Do not provide explanations.

User question:
{input}
"""


# === Run Prompt Version ===

def run_prompt_version(
    prompt_template: str,
) -> list[bool]:
    """Runs all test cases using one prompt version."""

    results = []

    for test_case in test_cases:

        prompt = prompt_template.format(
            input=test_case["input"]
        )

        response, error = call_model(prompt)

        result = evaluate_response(
            response,
            error,
            test_case["expected"],
        )

        results.append(result)

    return results


# === Run Regression Test ===

print("=== Prompt Regression Testing ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


# --- Baseline ---

print("\n=== Baseline Prompt ===")

baseline_results = run_prompt_version(
    baseline_prompt
)

for index, test_case in enumerate(
    test_cases,
    start=1,
):
    result = baseline_results[index - 1]

    print(
        f"--- Test {index}: "
        f"{test_case['name']} ---"
    )

    print(f"[Expected] {test_case['expected']}")

    if result:
        print("[Baseline Result] PASS")
    else:
        print("[Baseline Result] FAIL")


# --- Changed Prompt ---

print("\n=== Changed Prompt ===")

changed_results = run_prompt_version(
    changed_prompt
)

for index, test_case in enumerate(
    test_cases,
    start=1,
):
    result = changed_results[index - 1]

    print(
        f"--- Test {index}: "
        f"{test_case['name']} ---"
    )

    print(f"[Expected] {test_case['expected']}")

    if result:
        print("[Changed Result] PASS")
    else:
        print("[Changed Result] FAIL")


# === Regression Detection ===

print("\n=== Regression Detection ===")

regressions = 0

for index, test_case in enumerate(
    test_cases,
    start=1,
):
    baseline_result = baseline_results[index - 1]
    changed_result = changed_results[index - 1]

    if baseline_result and not changed_result:

        print(
            f"[REGRESSION] Test {index}: "
            f"{test_case['name']}"
        )

        print(
            "Previously PASS -> Now FAIL"
        )

        regressions += 1


# === Summary ===

baseline_passed = sum(baseline_results)
changed_passed = sum(changed_results)

total = len(test_cases)

print("\n=== Prompt Regression Summary ===")

print(f"Total Tests:       {total}")
print(f"Baseline Passed:   {baseline_passed}")
print(f"Changed Passed:    {changed_passed}")
print(f"Regressions:       {regressions}")

if regressions == 0:
    print("[Overall Result] NO REGRESSIONS")
else:
    print("[Overall Result] REGRESSION DETECTED")
