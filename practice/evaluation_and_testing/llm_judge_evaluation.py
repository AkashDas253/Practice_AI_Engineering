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


# === LLM Judge ===

def judge_response(
    response: str,
    criteria: list[str],
) -> tuple[bool, str]:
    """Uses an LLM to evaluate a response against defined criteria."""

    criteria_text = "\n".join(
        f"- {criterion}"
        for criterion in criteria
    )

    judge_prompt = f"""
You are evaluating an AI-generated response.

Response to evaluate:
{response}

Evaluation criteria:
{criteria_text}

Evaluate the response against all criteria.

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
# Add new test cases here without changing the evaluation loop.

test_cases = [
    {
        "name": "Clear Technical Explanation",
        "prompt": """
Explain what an API is to a beginner.
Keep the explanation concise and include one simple example.
""",
        "criteria": [
            "The explanation must be understandable to a beginner.",
            "The explanation must correctly describe the purpose of an API.",
            "The response must include one simple example.",
            "The response should be reasonably concise.",
        ],
    },
    {
        "name": "Useful Python Explanation",
        "prompt": """
Explain what a Python function is.
Give a simple explanation and a small example.
""",
        "criteria": [
            "The explanation must correctly describe what a Python function is.",
            "The explanation must be understandable to a beginner.",
            "The response must include a Python example.",
            "The example should be relevant to the explanation.",
        ],
    },
    {
        "name": "Criteria Violation",
        "prompt": """
Explain what an API is.
Give only a one-word answer.
""",
        "criteria": [
            "The response must explain what an API is.",
            "The response must contain enough information to be useful.",
            "The response must not consist of only one word.",
        ],
    },
]


# === Run Evaluation ===

print("=== LLM Judge Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    actual = call_model(test_case["prompt"])
    criteria = test_case["criteria"]

    result, reason = judge_response(
        actual,
        criteria,
    )

    print("[Response]")
    print(actual)

    print("\n[Criteria]")

    for criterion in criteria:
        print(f"- {criterion}")

    print(f"\n[Judge Reason] {reason}")

    if result:
        print("[Result]       PASS")
        passed += 1
    else:
        print("[Result]       FAIL")
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
