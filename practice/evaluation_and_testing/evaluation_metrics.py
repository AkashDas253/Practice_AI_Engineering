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


# === Response Evaluation ===

def evaluate_response(
    actual: str,
    expected: str,
) -> bool:
    """Checks whether the model response matches the expected answer."""

    return actual.strip().lower() == expected.strip().lower()


# === Evaluation Test Cases ===
#
# These cases are used to generate evaluation results.

evaluation_cases = [
    {
        "name": "Arithmetic",
        "prompt": "What is 2 + 2? Reply with only the number.",
        "expected": "4",
    },
    {
        "name": "Capital City",
        "prompt": "What is the capital of France? Reply with only the city name.",
        "expected": "Paris",
    },
    {
        "name": "Programming Language",
        "prompt": "Is Python a programming language? Reply with only Yes or No.",
        "expected": "Yes",
    },
]


# === Run Evaluation ===

print("=== Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(evaluation_cases)}")

evaluation_results = []

for index, test_case in enumerate(evaluation_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    expected = test_case["expected"]

    passed = evaluate_response(
        actual,
        expected,
    )

    print(f"[Expected] {expected}")
    print(f"[Actual]   {actual}")

    if passed:
        print("[Result]   PASS")
    else:
        print("[Result]   FAIL")

    evaluation_results.append(
        {
            "name": test_case["name"],
            "passed": passed,
        }
    )


# === Pass Rate ===

def calculate_pass_rate(
    results: list[dict],
) -> float:
    """Calculates the percentage of evaluations that passed."""

    if not results:
        return 0.0

    passed = sum(
        result["passed"]
        for result in results
    )

    return (passed / len(results)) * 100


# === Failure Rate ===

def calculate_failure_rate(
    results: list[dict],
) -> float:
    """Calculates the percentage of evaluations that failed."""

    if not results:
        return 0.0

    failed = sum(
        not result["passed"]
        for result in results
    )

    return (failed / len(results)) * 100


# === Average Score ===
#
# Separate score-based results are used because average score
# requires numerical evaluation scores.

score_results = [
    {
        "name": "Explanation",
        "score": 5,
    },
    {
        "name": "Example",
        "score": 4,
    },
    {
        "name": "Completeness",
        "score": 3,
    },
]


def calculate_average_score(
    results: list[dict],
) -> float:
    """Calculates the average evaluation score."""

    if not results:
        return 0.0

    total_score = sum(
        result["score"]
        for result in results
    )

    return total_score / len(results)


# === Metric Tests ===
#
# Each metric is tested independently using different result sets.


pass_rate_tests = [
    {
        "name": "All Passed",
        "results": [
            {"passed": True},
            {"passed": True},
            {"passed": True},
        ],
        "expected": 100.0,
    },
    {
        "name": "Mixed Results",
        "results": [
            {"passed": True},
            {"passed": False},
            {"passed": True},
            {"passed": False},
        ],
        "expected": 50.0,
    },
    {
        "name": "All Failed",
        "results": [
            {"passed": False},
            {"passed": False},
        ],
        "expected": 0.0,
    },
]


failure_rate_tests = [
    {
        "name": "No Failures",
        "results": [
            {"passed": True},
            {"passed": True},
            {"passed": True},
        ],
        "expected": 0.0,
    },
    {
        "name": "Mixed Results",
        "results": [
            {"passed": True},
            {"passed": False},
            {"passed": True},
            {"passed": False},
        ],
        "expected": 50.0,
    },
    {
        "name": "All Failed",
        "results": [
            {"passed": False},
            {"passed": False},
        ],
        "expected": 100.0,
    },
]


average_score_tests = [
    {
        "name": "All Same Score",
        "results": [
            {"score": 5},
            {"score": 5},
            {"score": 5},
        ],
        "expected": 5.0,
    },
    {
        "name": "Mixed Scores",
        "results": [
            {"score": 5},
            {"score": 4},
            {"score": 3},
        ],
        "expected": 4.0,
    },
    {
        "name": "Low Scores",
        "results": [
            {"score": 1},
            {"score": 2},
        ],
        "expected": 1.5,
    },
]


# === Run Pass Rate Tests ===

print("\n=== Pass Rate Tests ===")

for test in pass_rate_tests:

    actual = calculate_pass_rate(test["results"])
    expected = test["expected"]

    result = actual == expected

    print(f"{test['name']}: {actual:.2f}%")

    if result:
        print("[Result] PASS")
    else:
        print("[Result] FAIL")


# === Run Failure Rate Tests ===

print("\n=== Failure Rate Tests ===")

for test in failure_rate_tests:

    actual = calculate_failure_rate(test["results"])
    expected = test["expected"]

    result = actual == expected

    print(f"{test['name']}: {actual:.2f}%")

    if result:
        print("[Result] PASS")
    else:
        print("[Result] FAIL")


# === Run Average Score Tests ===

print("\n=== Average Score Tests ===")

for test in average_score_tests:

    actual = calculate_average_score(test["results"])
    expected = test["expected"]

    result = actual == expected

    print(f"{test['name']}: {actual:.2f}/5")

    if result:
        print("[Result] PASS")
    else:
        print("[Result] FAIL")


# === Evaluation Metrics ===

print("\n=== Evaluation Metrics ===")

pass_rate = calculate_pass_rate(
    evaluation_results
)

failure_rate = calculate_failure_rate(
    evaluation_results
)

average_score = calculate_average_score(
    score_results
)

print(f"Pass Rate:     {pass_rate:.2f}%")
print(f"Failure Rate:  {failure_rate:.2f}%")
print(f"Average Score: {average_score:.2f}/5")
