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


# Define tool
def check_shipping_status(order_id: int) -> str:
    """Checks the shipping status of an order."""

    print("\n[Tool Call] check_shipping_status")
    print(f"[Tool Arguments] order_id={order_id}")

    # Simulate a temporary timeout
    if not hasattr(check_shipping_status, "attempts"):
        check_shipping_status.attempts = 0

    check_shipping_status.attempts += 1

    if check_shipping_status.attempts < 3:
        raise TimeoutError("Shipping service timed out.")

    result = f"Order {order_id} is shipped and arriving tomorrow."

    print(f"[Tool Result] {result}")

    return result


# Retry the tool after temporary failures
def execute_with_retry(order_id: int, max_retries: int = 3) -> str:

    for attempt in range(1, max_retries + 1):

        print(f"\n[Attempt {attempt}/{max_retries}]")

        try:
            result = check_shipping_status(order_id)

            print("[Tool Execution Successful]")

            return result

        except TimeoutError as error:
            print(f"[Tool Error] {error}")

            if attempt == max_retries:
                return (
                    "Tool failed after all retry attempts. "
                    "Shipping status is currently unavailable."
                )

            print("[Retrying...]")
            time.sleep(1)

        except Exception as error:
            print(f"[Unexpected Tool Error] {error}")
            return "Tool failed due to an unexpected error."

    return "Tool execution failed."


# Disable automatic tool execution
config = types.GenerateContentConfig(
    tools=[check_shipping_status],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with retry handling...")
chat = client.chats.create(model=model, config=config)


# Send request requiring a tool
prompt = "What is the shipping status of order 9482?"
print(f"\n--- Test: Shipping Status ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Inspect tool call
if response.function_calls:
    for call in response.function_calls:

        print(f"\n[Tool Request] {call.name}")
        print(f"[Model Arguments] {call.args}")

        if call.name == "check_shipping_status":

            # Execute tool with retry handling
            result = execute_with_retry(
                order_id=call.args["order_id"]
            )

            # Send final result back to the model
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

else:
    print("\nNo tool call was requested.")
    print(response.text)

time.sleep(0.5)
