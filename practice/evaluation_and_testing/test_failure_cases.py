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


# === API Error Tests ===

def evaluate_api_error(
    response: str,
    error: str | None,
) -> bool:
    """Passes when the API correctly returns an error."""

    return error is not None


api_error_tests = [
    {
        "name": "Empty Input",
        "prompt": "",
    },
]


# === Unanswerable Request Tests ===

def evaluate_unanswerable_request(
    response: str,
    error: str | None,
) -> bool:
    """Checks whether the model recognizes missing information."""

    if error is not None:
        return False

    response_lower = response.lower()

    keywords = [
        "indeterminate",
        "unknown",
        "cannot determine",
        "can't determine",
        "cannot be determined",
        "can't be determined",
        "not enough information",
        "insufficient information",
        "unable to determine",
        "cannot answer",
        "can't answer",
        "unable to answer",
        "missing information",
        "missing context",
        "no context",
        "please provide",
        "forgot to include",
    ]

    return any(
        keyword in response_lower
        for keyword in keywords
    )


unanswerable_tests = [
    {
        "name": "Unknown Number",
        "prompt": (
            "What is the exact value of x if I give you "
            "no equation, no value for x, and no other information?"
        ),
    },
    {
        "name": "Missing Context",
        "prompt": (
            "What is the correct answer to the question?"
        ),
    },
]


# === Invalid Request Tests ===

def evaluate_invalid_request(
    response: str,
    error: str | None,
) -> bool:
    """Checks whether the model recognizes invalid input."""

    if error is not None:
        return True

    response_lower = response.lower()

    keywords = [
        "invalid",
        "invalid syntax",
        "syntax error",
        "syntactically invalid",
        "malformed",
        "not valid",
        "mathematically invalid",
        "invalid expression",
        "invalid arithmetic",
        "cannot be calculated as written",
        "can't be calculated as written",
        "cannot calculate as written",
        "can't calculate as written",
        "cannot be evaluated as written",
        "can't be evaluated as written",
        "cannot be evaluated",
        "can't be evaluated",
        "cannot be calculated",
        "can't be calculated",
        "consecutive operators",
        "missing operand",
        "missing number",
        "missing value",
        "operator without an operand",
        "two consecutive operators",
    ]

    return any(
        keyword in response_lower
        for keyword in keywords
    )


invalid_request_tests = [
    {
        "name": "Invalid Arithmetic",
        "prompt": "Calculate 10 +++ * / 5.",
    },
    {
        "name": "Missing Operand",
        "prompt": "Calculate 25 + * 7.",
    },
]


# === Test Runner ===

def run_tests(
    title: str,
    test_cases: list[dict],
    evaluator,
) -> tuple[int, int, int]:
    """Runs one group of failure tests."""

    print(f"\n=== {title} ===")
    print(f"Test cases: {len(test_cases)}")

    passed = 0
    failed = 0

    for index, test_case in enumerate(
        test_cases,
        start=1,
    ):
        print(
            f"\n--- Test {index}: "
            f"{test_case['name']} ---"
        )

        prompt = test_case["prompt"]

        print(f"[Input] {repr(prompt)}")

        response, error = call_model(prompt)

        if error is not None:
            print("[API Error]")
            print(error)
        else:
            print("[Response]")
            print(response)

        result = evaluator(
            response,
            error,
        )

        if result:
            print("[Result] PASS")
            passed += 1
        else:
            print("[Result] FAIL")
            failed += 1

    total = len(test_cases)

    return total, passed, failed


# === Run Evaluation ===

print("=== Failure Case Testing ===")
print(f"Model: {model}")

total = 0
passed = 0
failed = 0


# --- API Error Tests ---

test_total, test_passed, test_failed = run_tests(
    "API Error Tests",
    api_error_tests,
    evaluate_api_error,
)

total += test_total
passed += test_passed
failed += test_failed


# --- Unanswerable Request Tests ---

test_total, test_passed, test_failed = run_tests(
    "Unanswerable Request Tests",
    unanswerable_tests,
    evaluate_unanswerable_request,
)

total += test_total
passed += test_passed
failed += test_failed


# --- Invalid Request Tests ---

test_total, test_passed, test_failed = run_tests(
    "Invalid Request Tests",
    invalid_request_tests,
    evaluate_invalid_request,
)

total += test_total
passed += test_passed
failed += test_failed


# === Summary ===

print("\n=== Failure Case Evaluation Summary ===")

print(f"Total:  {total}")
print(f"Passed: {passed}")
print(f"Failed: {failed}")

if total > 0:
    pass_rate = (passed / total) * 100
else:
    pass_rate = 0.0

print(f"Pass Rate: {pass_rate:.2f}%")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
