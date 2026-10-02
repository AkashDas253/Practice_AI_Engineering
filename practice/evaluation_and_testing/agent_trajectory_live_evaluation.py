import json
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Config

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# Tools

def get_weather(city: str) -> dict:
    """Returns simulated weather information."""

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
    }

    return weather_data.get(
        city,
        {
            "city": city,
            "temperature_c": 25,
            "condition": "Unknown",
        },
    )


def calculate(expression: str) -> dict:
    """Calculates a simple arithmetic expression."""

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return {
            "expression": expression,
            "result": result,
        }

    except Exception as error:
        return {
            "expression": expression,
            "error": str(error),
        }


available_tools = {
    "get_weather": get_weather,
    "calculate": calculate,
}


# Tell Gemini what tools are available

get_weather_declaration = types.FunctionDeclaration(
    name="get_weather",
    description="Gets the current weather for a city.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "city": {
                "type": "STRING",
                "description": "The city name.",
            }
        },
        "required": ["city"],
    },
)

calculate_declaration = types.FunctionDeclaration(
    name="calculate",
    description="Calculates a basic arithmetic expression.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "expression": {
                "type": "STRING",
                "description": "A simple arithmetic expression.",
            }
        },
        "required": ["expression"],
    },
)

tools = [
    types.Tool(
        function_declarations=[
            get_weather_declaration,
            calculate_declaration,
        ]
    )
]


# Run the live agent and record its trajectory

def run_live_agent(task: str) -> tuple[list[dict], str, str | None]:

    trajectory = []

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=task)
            ],
        )
    ]

    step_number = 1

    try:
        while True:

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            candidate = response.candidates[0]

            function_calls = []

            for part in candidate.content.parts:
                if part.function_call:
                    function_calls.append(part.function_call)

            # No tool call means the agent is finished

            if not function_calls:

                final_answer = response.text.strip()

                trajectory.append(
                    {
                        "step": step_number,
                        "type": "final_answer",
                        "answer": final_answer,
                    }
                )

                return trajectory, final_answer, None

            contents.append(candidate.content)

            # Execute each requested tool

            for function_call in function_calls:

                tool_name = function_call.name
                arguments = dict(function_call.args)

                trajectory.append(
                    {
                        "step": step_number,
                        "type": "tool_call",
                        "tool": tool_name,
                        "arguments": arguments,
                    }
                )

                step_number += 1

                if tool_name not in available_tools:
                    return (
                        trajectory,
                        "",
                        f"Unknown tool requested: {tool_name}",
                    )

                tool_function = available_tools[tool_name]

                tool_result = tool_function(**arguments)

                trajectory.append(
                    {
                        "step": step_number,
                        "type": "tool_result",
                        "result": tool_result,
                    }
                )

                step_number += 1

                # Send the tool result back to Gemini

                function_response_part = (
                    types.Part.from_function_response(
                        name=tool_name,
                        response=tool_result,
                    )
                )

                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            function_response_part
                        ],
                    )
                )

    except Exception as error:
        return trajectory, "", str(error)


# Evaluate the actual trajectory

def evaluate_trajectory(
    trajectory: list[dict],
) -> tuple[bool, list[str]]:

    issues = []

    tool_calls = [
        step
        for step in trajectory
        if step["type"] == "tool_call"
    ]

    final_answers = [
        step
        for step in trajectory
        if step["type"] == "final_answer"
    ]

    # Check weather tool call

    weather_calls = [
        step
        for step in tool_calls
        if step["tool"] == "get_weather"
    ]

    if not weather_calls:
        issues.append("Agent did not call get_weather.")
    else:
        city = weather_calls[0]["arguments"].get("city")

        if city != "Kolkata":
            issues.append(
                f"Agent used incorrect city: {city}"
            )

    # Check calculation tool call

    calculation_calls = [
        step
        for step in tool_calls
        if step["tool"] == "calculate"
    ]

    if not calculation_calls:
        issues.append("Agent did not call calculate.")
    else:
        expression = calculation_calls[0]["arguments"].get(
            "expression"
        )

        if expression != "30 + 5":
            issues.append(
                f"Unexpected calculation expression: {expression}"
            )

    # Check final answer

    if not final_answers:
        issues.append("Agent did not produce a final answer.")
    else:
        final_answer = final_answers[-1]["answer"].lower()

        if "35" not in final_answer:
            issues.append(
                "Final answer does not contain the expected result 35."
            )

    return len(issues) == 0, issues


# Run the evaluation

task = (
    "Find the current temperature in Kolkata "
    "and add 5 degrees to it."
)

print("=== Live Agent Trajectory Evaluation ===")
print(f"Model: {model}")
print("Test cases: 1")

print("\n--- Test 1: Weather And Calculation Task ---")
print(f"[Task] {task}")


trajectory, final_answer, error = run_live_agent(task)


# Print the actual trajectory

print("\n=== Actual Live Trajectory ===")

for step in trajectory:
    print(json.dumps(step, indent=2))


# Handle execution errors

if error is not None:

    print("\n[Result] FAIL")
    print("[Evaluation] Live agent execution failed.")
    print(f"[Error] {error}")

    print("\n=== Agent Trajectory Evaluation Summary ===")
    print("Total Tests:   1")
    print("Passed:        0")
    print("Failed:        1")
    print("Pass Rate:     0.00%")
    print("[Overall Result] FAIL")

    raise SystemExit(1)


# Evaluate the trajectory

passed, issues = evaluate_trajectory(trajectory)

if passed:
    print("\n[Result] PASS")
    print(
        "[Evaluation] Live agent followed the expected "
        "tool-use trajectory and completed the task."
    )
else:
    print("\n[Result] FAIL")
    print("[Evaluation] Trajectory evaluation failed.")

    for issue in issues:
        print(f"[Issue] {issue}")


# Summary

total = 1
passed_count = 1 if passed else 0
failed_count = 0 if passed else 1

pass_rate = (passed_count / total) * 100

print("\n=== Agent Trajectory Evaluation Summary ===")
print(f"Total Tests:   {total}")
print(f"Passed:        {passed_count}")
print(f"Failed:        {failed_count}")
print(f"Pass Rate:     {pass_rate:.2f}%")

if failed_count == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
