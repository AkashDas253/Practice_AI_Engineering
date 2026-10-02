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
    Normalizes a response before consistency comparison.

    Removes harmless differences caused by:
    - capitalization
    - extra whitespace
    - Markdown bold
    - Markdown italic
    - backticks
    - common punctuation
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


# === Consistency Evaluation ===

def evaluate_consistency(
    responses: list[str],
) -> bool:
    """
    Passes when all successful responses are
    equivalent after normalization.
    """

    if not responses:
        return False

    normalized_responses = [
        normalize_response(response)
        for response in responses
    ]

    return len(set(normalized_responses)) == 1


# === Test Cases ===

test_cases = [
    {
        "name": "Simple Arithmetic",
        "prompt": "What is 2 + 2?",
        "runs": 3,
    },
    {
        "name": "Capital City",
        "prompt": "What is the capital of France?",
        "runs": 3,
    },
    {
        "name": "Programming Language",
        "prompt": (
            "Is Python a programming language? "
            "Answer only Yes or No."
        ),
        "runs": 3,
    },
]


# === Run Consistency Tests ===

print("=== Consistency Testing ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


total = 0
passed = 0
failed = 0


for test_case in test_cases:

    print(f"\n=== {test_case['name']} ===")

    prompt = test_case["prompt"]
    runs = test_case["runs"]

    print(f"[Prompt] {prompt}")
    print(f"[Runs]   {runs}")

    responses = []

    for run_number in range(1, runs + 1):

        print(f"\n--- Run {run_number} ---")

        response, error = call_model(prompt)

        if error is not None:
            print("[API Error]")
            print(error)
            continue

        print("[Response]")
        print(response)

        print("[Normalized]")
        print(normalize_response(response))

        responses.append(response)

    # === Evaluate ===

    result = evaluate_consistency(responses)

    if result:
        print("\n[Result] PASS")
        print("[Consistency] Responses are consistent.")
        passed += 1
    else:
        print("\n[Result] FAIL")
        print("[Consistency] Responses differ.")
        failed += 1

    total += 1


# === Summary ===

print("\n=== Consistency Evaluation Summary ===")

print(f"Total Tests:       {total}")
print(f"Consistent:        {passed}")
print(f"Inconsistent:      {failed}")

if total > 0:
    consistency_rate = (passed / total) * 100
else:
    consistency_rate = 0.0

print(f"Consistency Rate:  {consistency_rate:.2f}%")

if failed == 0:
    print("[Overall Result] CONSISTENT")
else:
    print("[Overall Result] INCONSISTENT")
