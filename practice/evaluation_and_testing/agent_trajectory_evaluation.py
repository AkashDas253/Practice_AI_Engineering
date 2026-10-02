import json


# === Mock Tools ===

def get_weather(city: str) -> dict:
    """Returns deterministic mock weather data."""

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

    if city not in weather_data:
        raise ValueError(
            f"Weather data is not available for {city}."
        )

    return weather_data[city]


def calculate(expression: str) -> dict:
    """Returns deterministic calculation results."""

    calculations = {
        "30 + 5": 35,
        "18 + 2": 20,
        "25 * 4": 100,
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
    """Executes a mock tool."""

    try:

        if tool_name == "get_weather":
            return (
                get_weather(arguments["city"]),
                None,
            )

        if tool_name == "calculate":
            return (
                calculate(arguments["expression"]),
                None,
            )

        return None, f"Unknown tool: {tool_name}"

    except Exception as error:
        return None, str(error)


# === Agent Trajectory ===

def run_agent(task: str) -> list[dict]:
    """
    Simulates an agent completing a task.

    The trajectory records each decision, tool call,
    tool result, and final answer.
    """

    trajectory = []

    # Step 1: Agent receives the task
    trajectory.append(
        {
            "step": 1,
            "type": "decision",
            "description": (
                "Agent identifies that it needs "
                "weather information for Kolkata."
            ),
        }
    )

    # Step 2: Agent calls weather tool
    weather_tool = {
        "step": 2,
        "type": "tool_call",
        "tool": "get_weather",
        "arguments": {
            "city": "Kolkata",
        },
    }

    trajectory.append(weather_tool)

    # Execute weather tool
    weather_result, weather_error = execute_tool(
        weather_tool["tool"],
        weather_tool["arguments"],
    )

    if weather_error:
        trajectory.append(
            {
                "step": 3,
                "type": "tool_error",
                "error": weather_error,
            }
        )

        return trajectory

    # Step 3: Record weather result
    trajectory.append(
        {
            "step": 3,
            "type": "tool_result",
            "result": weather_result,
        }
    )

    # Step 4: Agent decides it needs a calculation
    trajectory.append(
        {
            "step": 4,
            "type": "decision",
            "description": (
                "Agent decides to add 5 degrees "
                "to the reported temperature."
            ),
        }
    )

    # Step 5: Agent calls calculator
    calculation_tool = {
        "step": 5,
        "type": "tool_call",
        "tool": "calculate",
        "arguments": {
            "expression": "30 + 5",
        },
    }

    trajectory.append(calculation_tool)

    # Execute calculator
    calculation_result, calculation_error = execute_tool(
        calculation_tool["tool"],
        calculation_tool["arguments"],
    )

    if calculation_error:
        trajectory.append(
            {
                "step": 6,
                "type": "tool_error",
                "error": calculation_error,
            }
        )

        return trajectory

    # Step 6: Record calculation result
    trajectory.append(
        {
            "step": 6,
            "type": "tool_result",
            "result": calculation_result,
        }
    )

    # Step 7: Agent produces final answer
    trajectory.append(
        {
            "step": 7,
            "type": "final_answer",
            "answer": (
                "The current temperature in Kolkata is "
                "30°C. Adding 5°C gives 35°C."
            ),
        }
    )

    return trajectory


# === Trajectory Evaluation ===

def evaluate_trajectory(
    trajectory: list[dict],
    expected_trajectory: list[dict],
) -> tuple[bool, list[str]]:
    """
    Evaluates whether the agent followed the expected
    sequence of decisions, tool calls, and results.
    """

    errors = []

    if len(trajectory) != len(expected_trajectory):
        errors.append(
            "Trajectory length does not match the expected trajectory."
        )

    comparison_length = min(
        len(trajectory),
        len(expected_trajectory),
    )

    for index in range(comparison_length):

        actual = trajectory[index]
        expected = expected_trajectory[index]

        if actual.get("type") != expected.get("type"):
            errors.append(
                f"Step {index + 1}: expected type "
                f"'{expected.get('type')}', "
                f"got '{actual.get('type')}'."
            )
            continue

        if actual.get("type") == "tool_call":

            if actual.get("tool") != expected.get("tool"):
                errors.append(
                    f"Step {index + 1}: expected tool "
                    f"'{expected.get('tool')}', "
                    f"got '{actual.get('tool')}'."
                )

            if actual.get("arguments") != expected.get(
                "arguments"
            ):
                errors.append(
                    f"Step {index + 1}: tool arguments "
                    "do not match."
                )

        elif actual.get("type") == "tool_result":

            if actual.get("result") != expected.get(
                "result"
            ):
                errors.append(
                    f"Step {index + 1}: tool result "
                    "does not match."
                )

        elif actual.get("type") == "decision":

            if actual.get("description") != expected.get(
                "description"
            ):
                errors.append(
                    f"Step {index + 1}: decision "
                    "does not match."
                )

        elif actual.get("type") == "final_answer":

            if actual.get("answer") != expected.get(
                "answer"
            ):
                errors.append(
                    f"Step {index + 1}: final answer "
                    "does not match."
                )

    return len(errors) == 0, errors


# === Test Cases ===

test_cases = [
    {
        "name": "Weather And Calculation Task",
        "task": (
            "Find the current temperature in Kolkata "
            "and add 5 degrees to it."
        ),
        "expected_trajectory": [
            {
                "step": 1,
                "type": "decision",
                "description": (
                    "Agent identifies that it needs "
                    "weather information for Kolkata."
                ),
            },
            {
                "step": 2,
                "type": "tool_call",
                "tool": "get_weather",
                "arguments": {
                    "city": "Kolkata",
                },
            },
            {
                "step": 3,
                "type": "tool_result",
                "result": {
                    "city": "Kolkata",
                    "temperature_c": 30,
                    "condition": "Sunny",
                },
            },
            {
                "step": 4,
                "type": "decision",
                "description": (
                    "Agent decides to add 5 degrees "
                    "to the reported temperature."
                ),
            },
            {
                "step": 5,
                "type": "tool_call",
                "tool": "calculate",
                "arguments": {
                    "expression": "30 + 5",
                },
            },
            {
                "step": 6,
                "type": "tool_result",
                "result": {
                    "expression": "30 + 5",
                    "result": 35,
                },
            },
            {
                "step": 7,
                "type": "final_answer",
                "answer": (
                    "The current temperature in Kolkata is "
                    "30°C. Adding 5°C gives 35°C."
                ),
            },
        ],
    },
]


# === Run Evaluation ===

print("=== Agent Trajectory Evaluation ===")
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

    task = test_case["task"]

    print(f"[Task] {task}")

    print("\n=== Expected Trajectory ===")

    for step in test_case["expected_trajectory"]:
        print(
            json.dumps(
                step,
                indent=2,
            )
        )

    print("\n=== Actual Trajectory ===")

    trajectory = run_agent(task)

    for step in trajectory:
        print(
            json.dumps(
                step,
                indent=2,
            )
        )

    # === Evaluate ===

    result, errors = evaluate_trajectory(
        trajectory,
        test_case["expected_trajectory"],
    )

    if result:

        print("\n[Result] PASS")
        print(
            "[Evaluation] Agent followed the expected "
            "trajectory."
        )

        passed += 1

    else:

        print("\n[Result] FAIL")
        print(
            "[Evaluation] Agent trajectory differed "
            "from the expected trajectory."
        )

        for error in errors:
            print(f"[Trajectory Error] {error}")

        failed += 1

    total += 1


# === Summary ===

print("\n=== Agent Trajectory Evaluation Summary ===")

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
