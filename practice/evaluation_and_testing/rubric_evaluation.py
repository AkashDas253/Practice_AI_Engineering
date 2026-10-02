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


# === Rubric Evaluators ===

def contains_terms(response: str, terms: list[str]) -> bool:
    """Checks whether all required terms appear in the response."""

    response_lower = response.lower()

    return all(
        term.lower() in response_lower
        for term in terms
    )


def minimum_length(response: str, minimum_words: int) -> bool:
    """Checks whether the response contains at least the required words."""

    word_count = len(response.split())

    return word_count >= minimum_words


def maximum_length(response: str, maximum_words: int) -> bool:
    """Checks whether the response stays within the word limit."""

    word_count = len(response.split())

    return word_count <= maximum_words


# === Rubric Selection ===

evaluators = {
    "contains_terms": contains_terms,
    "minimum_length": minimum_length,
    "maximum_length": maximum_length,
}


def evaluate_rubric(
    response: str,
    rubric: list[dict],
) -> tuple[bool, list[bool]]:
    """Evaluates a response against each rubric criterion."""

    results = []

    for criterion in rubric:

        evaluator = evaluators[criterion["type"]]

        if criterion["type"] == "contains_terms":
            result = evaluator(
                response,
                criterion["terms"],
            )

        elif criterion["type"] == "minimum_length":
            result = evaluator(
                response,
                criterion["minimum_words"],
            )

        elif criterion["type"] == "maximum_length":
            result = evaluator(
                response,
                criterion["maximum_words"],
            )

        results.append(result)

    return all(results), results


# === Test Cases ===
#
# Add new test cases here without changing the execution loop.

test_cases = [
    {
        "name": "API Explanation",
        "prompt": """
        Explain what an API is to a beginner.
        Include a simple example.
        Keep the explanation concise.
        """,
        "rubric": [
            {
                "description": "Mention what an API is",
                "type": "contains_terms",
                "terms": ["API"],
            },
            {
                "description": "Include a simple example",
                "type": "contains_terms",
                "terms": ["example"],
            },
            {
                "description": "Provide enough information",
                "type": "minimum_length",
                "minimum_words": 20,
            },
            {
                "description": "Keep the response concise",
                "type": "maximum_length",
                "maximum_words": 150,
            },
        ],
    },
    {
        "name": "Python Function Explanation",
        "prompt": """
        Explain what a Python function is to a beginner.
        Include a small Python example.
        """,
        "rubric": [
            {
                "description": "Mention Python",
                "type": "contains_terms",
                "terms": ["Python"],
            },
            {
                "description": "Mention functions",
                "type": "contains_terms",
                "terms": ["function"],
            },
            {
                "description": "Include a Python example",
                "type": "contains_terms",
                "terms": ["def"],
            },
            {
                "description": "Provide enough information",
                "type": "minimum_length",
                "minimum_words": 20,
            },
        ],
    },
    {
        "name": "Incomplete Response",
        "prompt": """
        Explain what an API is.
        Include an example and explain how it works.
        """,
        "rubric": [
            {
                "description": "Mention API",
                "type": "contains_terms",
                "terms": ["API"],
            },
            {
                "description": "Include an example",
                "type": "contains_terms",
                "terms": ["example"],
            },
            {
                "description": "Explain how it works",
                "type": "contains_terms",
                "terms": ["request", "response"],
            },
            {
                "description": "Provide enough information",
                "type": "minimum_length",
                "minimum_words": 30,
            },
        ],
    },
]


# === Run Evaluation ===

print("=== Rubric Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])

    result, criterion_results = evaluate_rubric(
        actual,
        test_case["rubric"],
    )

    print("[Response]")
    print(actual)

    print("\n[Rubric]")

    for criterion, criterion_result in zip(
        test_case["rubric"],
        criterion_results,
    ):
        status = "PASS" if criterion_result else "FAIL"

        print(
            f"- [{status}] "
            f"{criterion['description']}"
        )

    if result:
        print("[Result] PASS")
        passed += 1
    else:
        print("[Result] FAIL")
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
