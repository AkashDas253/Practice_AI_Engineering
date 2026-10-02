import os
import re
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


# === Normalization ===

def normalize_response(response: str) -> str:
    """
    Normalizes model output before comparison.

    Removes harmless differences caused by:
    - capitalization
    - Markdown formatting
    - punctuation
    - extra whitespace
    """

    text = response.lower().strip()

    # Remove Markdown formatting
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("*", "")
    text = text.replace("`", "")

    # Remove common punctuation
    text = re.sub(r"[.,!?;:]", "", text)

    # Normalize whitespace
    text = " ".join(text.split())

    return text.strip()


# === Evaluation ===

def evaluate_response(
    response: str,
    expected: str,
    error: str | None,
) -> bool:
    """Checks whether a response matches the expected answer."""

    if error is not None:
        return False

    if not response.strip():
        return False

    normalized_response = normalize_response(response)
    normalized_expected = normalize_response(expected)

    return normalized_response == normalized_expected


# === Test Dataset ===

test_cases = [
    {
        "name": "Simple Arithmetic",
        "prompt": "What is 2 + 2? Answer only the number.",
        "expected": "4",
    },
    {
        "name": "Capital City",
        "prompt": (
            "What is the capital of France? "
            "Answer only the city."
        ),
        "expected": "Paris",
    },
    {
        "name": "Programming Language",
        "prompt": (
            "Is Python a programming language? "
            "Answer only Yes or No."
        ),
        "expected": "Yes",
    },
    {
        "name": "Simple Multiplication",
        "prompt": "What is 5 * 6? Answer only the number.",
        "expected": "30",
    },
    {
        "name": "Largest Planet",
        "prompt": (
            "What is the largest planet in our solar system? "
            "Answer only the planet name."
        ),
        "expected": "Jupiter",
    },
]


# === System Versions ===

version_a_prefix = ""

version_b_prefix = (
    "Answer the user's question directly and concisely. "
    "Follow the requested output format exactly.\n\n"
)


# === Run Version ===

def run_version(
    version_name: str,
    prompt_prefix: str,
) -> tuple[int, int, list[dict]]:
    """
    Runs one system version against the complete dataset.

    Returns:
        total, passed, results
    """

    print(f"\n=== {version_name} ===")

    passed = 0
    results = []

    for index, test_case in enumerate(
        test_cases,
        start=1,
    ):

        name = test_case["name"]
        prompt = test_case["prompt"]
        expected = test_case["expected"]

        final_prompt = prompt_prefix + prompt

        print(
            f"\n--- Test {index}: {name} ---"
        )

        print(f"[Prompt]   {final_prompt}")
        print(f"[Expected] {expected}")

        response, error = call_model(final_prompt)

        if error is not None:

            print("[API Error]")
            print(error)

            result = False
            actual = ""

        else:

            actual = response

            print(f"[Actual]   {actual}")

            normalized_actual = normalize_response(actual)
            normalized_expected = normalize_response(expected)

            print(
                f"[Normalized Actual]   "
                f"{normalized_actual}"
            )

            print(
                f"[Normalized Expected] "
                f"{normalized_expected}"
            )

            result = evaluate_response(
                actual,
                expected,
                error,
            )

        if result:
            print("[Result] PASS")
            passed += 1
        else:
            print("[Result] FAIL")

        results.append(
            {
                "name": name,
                "expected": expected,
                "actual": actual,
                "error": error,
                "passed": result,
            }
        )

    total = len(test_cases)

    return total, passed, results


# === Run Comparison ===

print("=== Evaluation Comparison ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


# --- Version A ---

total_a, passed_a, results_a = run_version(
    "Version A - Baseline",
    version_a_prefix,
)


# --- Version B ---

total_b, passed_b, results_b = run_version(
    "Version B - Changed",
    version_b_prefix,
)


# === Calculate Rates ===

if total_a > 0:
    rate_a = (passed_a / total_a) * 100
else:
    rate_a = 0.0


if total_b > 0:
    rate_b = (passed_b / total_b) * 100
else:
    rate_b = 0.0


# === Test-by-Test Comparison ===

print("\n=== Test-by-Test Comparison ===")

changed_cases = 0
improved_cases = 0
regressed_cases = 0
unchanged_cases = 0


for result_a, result_b in zip(
    results_a,
    results_b,
):

    name = result_a["name"]

    status_a = result_a["passed"]
    status_b = result_b["passed"]

    print(f"\n--- {name} ---")

    print(
        f"Version A: "
        f"{'PASS' if status_a else 'FAIL'}"
    )

    print(
        f"Version B: "
        f"{'PASS' if status_b else 'FAIL'}"
    )

    if status_a == status_b:

        unchanged_cases += 1

        print("[Comparison] UNCHANGED")

    else:

        changed_cases += 1

        if not status_a and status_b:
            improved_cases += 1
            print("[Comparison] STATUS CHANGED")

        elif status_a and not status_b:
            regressed_cases += 1
            print("[Comparison] STATUS CHANGED")


# === Summary ===

print("\n=== Evaluation Comparison Summary ===")

print("\nVersion A - Baseline")
print(f"Total Tests:   {total_a}")
print(f"Passed:        {passed_a}")
print(f"Failed:        {total_a - passed_a}")
print(f"Pass Rate:     {rate_a:.2f}%")

print("\nVersion B - Changed")
print(f"Total Tests:   {total_b}")
print(f"Passed:        {passed_b}")
print(f"Failed:        {total_b - passed_b}")
print(f"Pass Rate:     {rate_b:.2f}%")

print("\n=== Change Summary ===")

print(f"Tests Changed:       {changed_cases}")
print(f"Tests Unchanged:     {unchanged_cases}")
print(f"Tests Improved:      {improved_cases}")
print(f"Tests Regressed:     {regressed_cases}")

rate_difference = rate_b - rate_a

print(
    f"Pass Rate Difference: "
    f"{rate_difference:+.2f} percentage points"
)


# === Final Status ===

print("\n=== Evaluation Status ===")

if regressed_cases > 0:
    print("[Status] REGRESSIONS DETECTED")

elif changed_cases > 0:
    print("[Status] RESULTS CHANGED")

else:
    print("[Status] RESULTS UNCHANGED")
