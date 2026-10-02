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

def call_model(prompt: str) -> tuple[str, str | None]:
    """Sends a prompt to the model and returns the response and error."""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text.strip(), None

    except Exception as error:
        return "", str(error)


# ============================================================
# === Empty Input =============================================
# ============================================================

def evaluate_empty_input(
    response: str,
    error: str | None,
) -> bool:
    """Checks whether empty input is rejected with an API error."""

    return error is not None


empty_input_tests = [
    {
        "name": "Empty String",
        "prompt": "",
    },
]


# ============================================================
# === Ambiguous Input =========================================
# ============================================================

def evaluate_ambiguous_input(
    response: str,
    error: str | None,
) -> bool:
    """
    Checks whether an ambiguous input receives a usable response.

    A vague prompt does not necessarily require clarification.
    The model may reasonably provide a general explanation.
    """

    if error is not None:
        return False

    return len(response.strip()) > 0


ambiguous_input_tests = [
    {
        "name": "Vague Python Request",
        "prompt": "Tell me about Python.",
    },
    {
        "name": "Vague Programming Request",
        "prompt": "Tell me about programming.",
    },
]


# ============================================================
# === Malformed Input =========================================
# ============================================================

def evaluate_malformed_input(
    response: str,
    error: str | None,
) -> bool:
    """Checks whether malformed input is handled appropriately."""

    if error is not None:
        return True

    response_lower = response.lower()

    keywords = [
        "invalid",
        "incorrect",
        "not valid",
        "syntax",
        "malformed",
        "cannot calculate",
        "can't calculate",
        "cannot be calculated",
        "can't be calculated",
        "not possible",
        "clarify",
    ]

    return any(
        keyword in response_lower
        for keyword in keywords
    )


malformed_input_tests = [
    {
        "name": "Invalid Arithmetic",
        "prompt": "Calculate 10 +++ * / 5.",
    },
    {
        "name": "Malformed Expression",
        "prompt": "What is 25 + * 7?",
    },
]


# ============================================================
# === Boundary Input ==========================================
# ============================================================

def evaluate_boundary_input(
    response: str,
    error: str | None,
) -> bool:
    """Checks whether a boundary input receives a usable response."""

    if error is not None:
        return False

    return len(response.strip()) > 0


boundary_input_tests = [
    {
        "name": "Smallest Positive Integer",
        "prompt": "What is the smallest positive integer?",
    },
    {
        "name": "Zero",
        "prompt": "What is 0 + 0?",
    },
]


# ============================================================
# === Test Runner =============================================
# ============================================================

def run_test_group(
    group_name: str,
    test_cases: list[dict],
    evaluator,
) -> tuple[int, int, int]:
    """
    Runs all tests in one edge-case group.

    Returns:
        total, passed, failed
    """

    print(f"\n=== {group_name} ===")
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


# ============================================================
# === Run Evaluation =========================================
# ============================================================

print("=== Edge Case Testing ===")
print(f"Model: {model}")


total = 0
passed = 0
failed = 0


# --- Empty Input ---

group_total, group_passed, group_failed = run_test_group(
    "Empty Input Tests",
    empty_input_tests,
    evaluate_empty_input,
)

total += group_total
passed += group_passed
failed += group_failed


# --- Ambiguous Input ---

group_total, group_passed, group_failed = run_test_group(
    "Ambiguous Input Tests",
    ambiguous_input_tests,
    evaluate_ambiguous_input,
)

total += group_total
passed += group_passed
failed += group_failed


# --- Malformed Input ---

group_total, group_passed, group_failed = run_test_group(
    "Malformed Input Tests",
    malformed_input_tests,
    evaluate_malformed_input,
)

total += group_total
passed += group_passed
failed += group_failed


# --- Boundary Input ---

group_total, group_passed, group_failed = run_test_group(
    "Boundary Input Tests",
    boundary_input_tests,
    evaluate_boundary_input,
)

total += group_total
passed += group_passed
failed += group_failed


# ============================================================
# === Summary =================================================
# ============================================================

print("\n=== Edge Case Evaluation Summary ===")

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
