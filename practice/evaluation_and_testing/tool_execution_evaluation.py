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


# === Tool Implementations ===

def get_weather(city: str) -> dict:
    """
    Simulates a weather tool.

    In a real application this could call a weather API.
    """

    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        },
        "Paris": {
            "city": "Paris",
            "temperature_c": 18,
            "condition": "Cloudy",
        },
        "London": {
            "city": "London",
            "temperature_c": 15,
            "condition": "Rainy",
        },
    }

    if city not in weather_data:
        raise ValueError(
            f"Weather data is not available for {city}."
        )

    return weather_data[city]


def calculate(expression: str) -> dict:
    """
    Simulates a calculator tool.

    Only a small set of known expressions is supported
    so that the evaluation remains deterministic.
    """

    calculations = {
        "25 * 4": 100,
        "10 + 5": 15,
        "20 - 7": 13,
        "36 / 6": 6,
    }

    if expression not in calculations:
        raise ValueError(
            f"Unsupported expression: {expression}"
        )

    return {
        "expression": expression,
        "result": calculations[expression],
    }


# === Tool Dispatcher ===

def execute_tool(
    tool_name: str,
    arguments: dict,
) -> tuple[dict | None, str | None]:
    """
    Executes the selected tool and returns:
    (result, error)
    """

    try:

        if tool_name == "get_weather":

            result = get_weather(
                arguments["city"]
            )

            return result, None

        if tool_name == "calculate":

            result = calculate(
                arguments["expression"]
            )

            return result, None

        return None, (
            f"Unknown tool: {tool_name}"
        )

    except Exception as error:

        return None, str(error)


# === Tool Execution Evaluation ===

def evaluate_tool_execution(
    actual_result: dict | None,
    error: str | None,
    expected_result: dict,
) -> bool:
    """
    Evaluates whether tool execution completed successfully
    and returned the expected result.
    """

    if error is not None:
        return False

    if actual_result is None:
        return False

    return actual_result == expected_result


# === Test Cases ===

test_cases = [
    {
        "name": "Weather Tool - Kolkata",
        "tool": "get_weather",
        "arguments": {
            "city": "Kolkata",
        },
        "expected_result": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        },
    },
    {
        "name": "Calculator Tool - Multiplication",
        "tool": "calculate",
        "arguments": {
            "expression": "25 * 4",
        },
        "expected_result": {
            "expression": "25 * 4",
            "result": 100,
        },
    },
    {
        "name": "Weather Tool - Paris",
        "tool": "get_weather",
        "arguments": {
            "city": "Paris",
        },
        "expected_result": {
            "city": "Paris",
            "temperature_c": 18,
            "condition": "Cloudy",
        },
    },
]


# === Run Evaluation ===

print("=== Tool Execution Evaluation ===")
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

    tool_name = test_case["tool"]
    arguments = test_case["arguments"]
    expected_result = test_case["expected_result"]

    print(f"[Tool] {tool_name}")
    print(
        "[Arguments] "
        f"{json.dumps(arguments)}"
    )
    print(
        "[Expected Result] "
        f"{json.dumps(expected_result)}"
    )

    actual_result, error = execute_tool(
        tool_name,
        arguments,
    )

    if error is not None:

        print("[Execution Error]")
        print(error)

    else:

        print(
            "[Actual Result] "
            f"{json.dumps(actual_result)}"
        )

    result = evaluate_tool_execution(
        actual_result,
        error,
        expected_result,
    )

    if result:

        print("[Result] PASS")
        print(
            "[Evaluation] Tool executed successfully "
            "and returned the expected result."
        )

        passed += 1

    else:

        print("[Result] FAIL")

        if error is not None:

            print(
                "[Evaluation] Tool execution "
                "returned an error."
            )

        elif actual_result != expected_result:

            print(
                "[Evaluation] Tool execution result "
                "did not match the expected result."
            )

        else:

            print(
                "[Evaluation] Tool execution "
                "could not be evaluated."
            )

        failed += 1

    total += 1


# === Summary ===

print("\n=== Tool Execution Evaluation Summary ===")

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
