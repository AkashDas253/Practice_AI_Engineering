import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# === Config ===

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# === Tool Definitions ===

tools = [
    types.Tool(
        function_declarations=[
            types.FunctionDeclaration(
                name="get_weather",
                description="Gets the current weather for a city.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "city": types.Schema(
                            type="STRING",
                            description="The city to get weather for.",
                        ),
                    },
                    required=["city"],
                ),
            ),
            types.FunctionDeclaration(
                name="calculate",
                description="Performs a mathematical calculation.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "expression": types.Schema(
                            type="STRING",
                            description="A mathematical expression to calculate.",
                        ),
                    },
                    required=["expression"],
                ),
            ),
        ]
    )
]


# === Model Call ===

def call_model(prompt: str):
    """Calls the model and extracts a function call."""

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=tools,
            ),
        )

        function_call = None

        for part in response.candidates[0].content.parts:
            if part.function_call:
                function_call = part.function_call
                break

        if function_call is None:
            return None, None, response.text, None

        return (
            function_call.name,
            dict(function_call.args),
            response.text,
            None,
        )

    except Exception as error:
        return None, None, "", str(error)


# === Tool Call Evaluation ===

def evaluate_tool_call(
    actual_tool: str | None,
    actual_arguments: dict | None,
    expected_tool: str,
    expected_arguments: dict,
) -> bool:
    """
    Evaluates whether the model selected the expected tool
    and generated the expected arguments.
    """

    if actual_tool != expected_tool:
        return False

    if actual_arguments is None:
        return False

    return actual_arguments == expected_arguments


# === Test Cases ===

test_cases = [
    {
        "name": "Weather Request",
        "prompt": "What is the weather in Kolkata?",
        "expected_tool": "get_weather",
        "expected_arguments": {
            "city": "Kolkata",
        },
    },
    {
        "name": "Calculation Request",
        "prompt": "Calculate 25 * 4.",
        "expected_tool": "calculate",
        "expected_arguments": {
            "expression": "25 * 4",
        },
    },
    {
        "name": "Another Weather Request",
        "prompt": "Tell me the current weather in Paris.",
        "expected_tool": "get_weather",
        "expected_arguments": {
            "city": "Paris",
        },
    },
]


# === Run Evaluation ===

print("=== Tool Call Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


total = 0
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

    expected_tool = test_case["expected_tool"]
    expected_arguments = test_case["expected_arguments"]

    print(f"[Prompt] {prompt}")
    print(f"[Expected Tool] {expected_tool}")
    print(
        "[Expected Arguments] "
        f"{json.dumps(expected_arguments)}"
    )

    (
        actual_tool,
        actual_arguments,
        response_text,
        error,
    ) = call_model(prompt)

    if error is not None:

        print("[API Error]")
        print(error)

        result = False

    else:

        if actual_tool is not None:

            print(f"[Actual Tool] {actual_tool}")
            print(
                "[Actual Arguments] "
                f"{json.dumps(actual_arguments)}"
            )

        else:

            print("[Actual Tool] None")
            print("[Actual Arguments] None")

            if response_text:
                print("[Model Response]")
                print(response_text)

        result = evaluate_tool_call(
            actual_tool,
            actual_arguments,
            expected_tool,
            expected_arguments,
        )

    if result:

        print("[Result] PASS")
        print(
            "[Evaluation] Correct tool selected "
            "and arguments matched."
        )

        passed += 1

    else:

        print("[Result] FAIL")

        if actual_tool != expected_tool:
            print(
                "[Evaluation] Tool selection did not match."
            )

        elif actual_arguments != expected_arguments:
            print(
                "[Evaluation] Tool arguments did not match."
            )

        else:
            print(
                "[Evaluation] Tool call could not be evaluated."
            )

        failed += 1

    total += 1


# === Summary ===

print("\n=== Tool Call Evaluation Summary ===")

print(f"Total Tests:   {total}")
print(f"Passed:        {passed}")
print(f"Failed:        {failed}")

if total > 0:
    pass_rate = (passed / total) * 100
else:
    pass_rate = 0.0

print(f"Pass Rate:     {pass_rate:.2f}%")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
