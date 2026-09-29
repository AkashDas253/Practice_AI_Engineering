import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env sitting in the same folder as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"


# Tool: Check task status
def check_task_status(task_id: int) -> str:
    """Checks the current status of a task."""

    print("\n[Tool Call] check_task_status")
    print(f"[Tool Arguments] task_id={task_id}")

    task_data = {
        101: "completed",
        202: "in_progress",
        303: "failed",
    }

    result = task_data.get(
        task_id,
        "unknown"
    )

    print(f"[Tool Result] Task {task_id}: {result}")

    return result


# Configure the agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a task monitoring agent. "
        "Check the task status and continue monitoring when necessary. "
        "Stop when the task succeeds or fails."
    ),
    tools=[check_task_status],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating agent with stop conditions...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Stop-condition settings
MAX_ITERATIONS = 5
TIME_LIMIT_SECONDS = 10

task_id = 202

print("\n=== TASK ===")
print(f"Monitor task #{task_id}")


start_time = time.time()
iteration = 0
stop_reason = None


# Start the agent loop
response = chat.send_message(
    f"""
Monitor task #{task_id}.

Stop when:
1. The task is completed.
2. The task fails.
3. The maximum number of iterations is reached.
4. The time limit is reached.

Check the task status when necessary.
"""
)


while True:

    # Check time limit
    elapsed_time = time.time() - start_time

    if elapsed_time >= TIME_LIMIT_SECONDS:
        stop_reason = "Time limit reached."
        break

    # Check iteration limit
    if iteration >= MAX_ITERATIONS:
        stop_reason = "Maximum iteration limit reached."
        break

    iteration += 1

    print(f"\n--- Agent Iteration {iteration} ---")

    if response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Action] {call.name}")
            print(f"[Arguments] {call.args}")

            if call.name == "check_task_status":

                result = check_task_status(**call.args)

                # Check for terminal states
                if "completed" in result:
                    stop_reason = "Task completed successfully."

                elif "failed" in result:
                    stop_reason = "Task failed."

                # Send observation back to the model
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )
                )

                # Stop after terminal result
                if stop_reason:
                    break

            else:

                result = "Unknown tool requested."

                response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )
                )

        if stop_reason:
            break

    else:

        # The model stopped requesting actions
        stop_reason = "Agent stopped requesting actions."
        break

    time.sleep(0.5)


print("\n=== STOP CONDITION ===")
print(stop_reason)

print("\n=== AGENT RESPONSE ===")
print(response.text)
