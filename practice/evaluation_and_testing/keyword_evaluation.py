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


# === Keyword Evaluators ===

def all_keywords_match(response: str, keywords: list[str]) -> bool:
    """Checks whether every required keyword appears in the response."""

    response_lower = response.lower()

    return all(
        keyword.lower() in response_lower
        for keyword in keywords
    )


def any_keyword_matches(response: str, keywords: list[str]) -> bool:
    """Checks whether at least one keyword appears in the response."""

    response_lower = response.lower()

    return any(
        keyword.lower() in response_lower
        for keyword in keywords
    )


# === Evaluator Selection ===

evaluators = {
    "all": all_keywords_match,
    "any": any_keyword_matches,
}


# === Test Cases ===
#
# Add new test cases here without changing the evaluation loop.

test_cases = [
    {
        "name": "Required Keyword",
        "prompt": "Explain what Python is in one sentence.",
        "keywords": ["Python"],
        "match_type": "all",
    },
    {
        "name": "Multiple Required Keywords",
        "prompt": "Explain what an API is and mention requests and responses.",
        "keywords": ["API", "request", "response"],
        "match_type": "all",
    },
    {
        "name": "Any Matching Keyword",
        "prompt": "Name one programming language.",
        "keywords": ["Python", "Java", "Go"],
        "match_type": "any",
    },
]


# === Run Evaluation ===

print("=== Keyword Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])

    keywords = test_case["keywords"]
    match_type = test_case["match_type"]

    evaluator = evaluators[match_type]

    result = evaluator(actual, keywords)

    print(f"[Match Type] {match_type}")
    print(f"[Keywords]   {keywords}")
    print(f"[Response]   {actual}")

    if result:
        print("[Result]     PASS")
        passed += 1
    else:
        print("[Result]     FAIL")
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
