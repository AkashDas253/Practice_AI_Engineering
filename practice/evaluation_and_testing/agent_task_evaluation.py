import json


# === Mock Agent Task ===

task = "Find the current temperature in Kolkata and add 5 degrees to it."


# === Expected Task Outcome ===

expected_result = {
    "city": "Kolkata",
    "original_temperature_c": 30,
    "added_degrees": 5,
    "final_temperature_c": 35,
}


# === Simulated Agent Execution ===

def run_agent_task() -> dict:
    """
    Simulates an agent completing the requested task.

    In a real system, this function would run the agent
    and collect its final result.
    """

    # Step 1: Get weather information
    weather_result = {
        "city": "Kolkata",
        "temperature_c": 30,
        "condition": "Sunny",
    }

    # Step 2: Perform calculation
    final_temperature = weather_result["temperature_c"] + 5

    # Step 3: Return the completed task result
    return {
        "city": weather_result["city"],
        "original_temperature_c": weather_result["temperature_c"],
        "added_degrees": 5,
        "final_temperature_c": final_temperature,
    }


# === Task Evaluation ===

def evaluate_task(
    actual_result: dict,
    expected_result: dict,
) -> bool:
    """
    Passes when the agent produced the expected
    final task result.
    """

    return actual_result == expected_result


# === Run Evaluation ===

print("=== Agent Task Evaluation ===")
print("Test cases: 1")


print("\n--- Test 1: Weather And Calculation Task ---")

print(f"[Task] {task}")

print("\n=== Expected Task Result ===")
print(json.dumps(expected_result, indent=2))


actual_result = run_agent_task()

print("\n=== Actual Task Result ===")
print(json.dumps(actual_result, indent=2))


# === Evaluate ===

result = evaluate_task(
    actual_result,
    expected_result,
)

if result:
    print("\n[Result] PASS")
    print(
        "[Evaluation] Agent completed the intended task "
        "and produced the expected result."
    )
else:
    print("\n[Result] FAIL")
    print(
        "[Evaluation] Agent did not produce the "
        "expected task result."
    )


# === Summary ===

total = 1
passed = 1 if result else 0
failed = 0 if result else 1

pass_rate = (passed / total) * 100

print("\n=== Agent Task Evaluation Summary ===")

print(f"Total Tests:   {total}")
print(f"Passed:        {passed}")
print(f"Failed:        {failed}")
print(f"Pass Rate:     {pass_rate:.2f}%")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
