import json
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


# === Quality Evaluation ===

def evaluate_quality(
    prompt: str,
    response: str,
) -> dict:
    """Evaluates a response for relevance, clarity, completeness, and correctness."""

    judge_prompt = f"""
Evaluate the following AI response.

User Prompt:
{prompt}

AI Response:
{response}

Evaluate these four qualities:

1. relevance
   - Does the response directly address the user's request?

2. clarity
   - Is the response easy to understand and well organized?

3. completeness
   - Does the response provide the important information needed to answer the request?

4. correctness
   - Is the information accurate and free from obvious factual errors?

For each quality, provide:
- score: an integer from 1 to 5
- reason: a short explanation

Return ONLY valid JSON using this structure:

{{
    "relevance": {{
        "score": 1,
        "reason": "..."
    }},
    "clarity": {{
        "score": 1,
        "reason": "..."
    }},
    "completeness": {{
        "score": 1,
        "reason": "..."
    }},
    "correctness": {{
        "score": 1,
        "reason": "..."
    }}
}}
"""

    result = call_model(judge_prompt)

    try:
        cleaned = result.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()

        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        return json.loads(cleaned)

    except json.JSONDecodeError:
        return {
            "error": "Judge returned invalid JSON",
            "raw_output": result,
        }


# === Test Cases ===
#
# Add new test cases here without changing the evaluation loop.

test_cases = [
    {
        "name": "Clear API Explanation",
        "prompt": "Explain what an API is to a beginner.",
        "response": """
        An API is a way for two software systems to communicate with each
        other. For example, a weather app can use a weather API to request
        the current temperature and display it to the user.
        """,
    },
    {
        "name": "Python Function Explanation",
        "prompt": "Explain what a Python function is and give a simple example.",
        "response": """
        A Python function is a reusable block of code that performs a
        specific task. For example:

        def greet(name):
            return f"Hello, {name}!"

        Calling greet("Alice") returns "Hello, Alice!".
        """,
    },
    {
        "name": "Incomplete Answer",
        "prompt": "Explain what an API is and give an example.",
        "response": """
        An API is an interface that allows software systems to communicate.
        """,
    },
]


# === Run Evaluation ===

print("=== Response Quality Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

passed = 0
failed = 0

quality_names = [
    "relevance",
    "clarity",
    "completeness",
    "correctness",
]

minimum_score = 3

for index, test_case in enumerate(test_cases, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    prompt = test_case["prompt"]
    response = test_case["response"]

    print("[Response]")
    print(response.strip())

    evaluation = evaluate_quality(
        prompt,
        response,
    )

    if "error" in evaluation:
        print("[Evaluation] FAIL")
        print(f"[Reason] {evaluation['error']}")
        failed += 1
        continue

    scores = []

    print("\n[Quality Scores]")

    for quality in quality_names:

        result = evaluation[quality]

        score = result["score"]
        reason = result["reason"]

        scores.append(score)

        print(f"- {quality.capitalize()}: {score}/5")
        print(f"  Reason: {reason}")

    average_score = sum(scores) / len(scores)

    passed_quality = all(
        score >= minimum_score
        for score in scores
    )

    print(f"\n[Average Score] {average_score:.2f}/5")

    if passed_quality:
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
