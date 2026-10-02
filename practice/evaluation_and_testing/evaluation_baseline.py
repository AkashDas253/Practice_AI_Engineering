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
    """Call the model and return response text and error."""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text.strip(), None

    except Exception as error:
        return "", str(error)


# === Normalization ===

def normalize_response(text: str) -> str:
    """
    Normalize harmless formatting differences.

    Examples:
        Yes      -> yes
        Yes.     -> yes
        **Yes**  -> yes
        `Yes`    -> yes
    """

    text = text.strip().lower()

    # Remove Markdown formatting
    text = text.replace("**", "")
    text = text.replace("__", "")
    text = text.replace("`", "")
    text = text.replace("*", "")

    # Remove punctuation
    text = re.sub(r"[.,!?;:]", "", text)

    # Normalize whitespace
    text = " ".join(text.split())

    return text.strip()


# === Evaluation ===

def evaluate_response(
    actual: str,
    expected: str,
    error: str | None,
) -> bool:
    """Compare normalized actual and expected responses."""

    if error is not None:
        return False

    normalized_actual = normalize_response(actual)
    normalized_expected = normalize_response(expected)

    print(f"[Normalized Actual]   {normalized_actual}")
    print(f"[Normalized Expected] {normalized_expected}")

    return normalized_actual == normalized_expected


# === Baseline Dataset ===

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


# === Run Baseline ===

print("=== Evaluation Baseline ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


passed = 0
failed = 0


for index, test_case in enumerate(test_cases, start=1):

    print(
        f"\n--- Test {index}: "
        f"{test_case['name']} ---"
    )

    prompt = test_case["prompt"]
    expected = test_case["expected"]

    print(f"[Prompt]   {prompt}")
    print(f"[Expected] {expected}")

    actual, error = call_model(prompt)

    if error is not None:
        print("[API Error]")
        print(error)

        result = False

    else:
        print(f"[Actual]   {actual}")

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
        failed += 1


# === Summary ===

total = len(test_cases)

if total > 0:
    pass_rate = (passed / total) * 100
else:
    pass_rate = 0.0


print("\n=== Baseline Evaluation Summary ===")
print(f"Total Tests:   {total}")
print(f"Passed:        {passed}")
print(f"Failed:        {failed}")
print(f"Pass Rate:     {pass_rate:.2f}%")


# === Baseline Record ===

print("\n=== Baseline Record ===")
print(f"Model:         {model}")
print(f"Total Tests:   {total}")
print(f"Passed:        {passed}")
print(f"Failed:        {failed}")
print(f"Pass Rate:     {pass_rate:.2f}%")

print("\n[Baseline Status] ESTABLISHED")
