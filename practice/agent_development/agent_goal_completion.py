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


# Tool: Check available inventory
def check_inventory(product: str) -> str:
    """Checks the available quantity of a product."""

    print("\n[Tool Call] check_inventory")
    print(f"[Tool Arguments] product={product}")

    inventory = {
        "laptop": 0,
        "tablet": 0,
        "phone": 10,
    }

    quantity = inventory.get(product.lower(), 0)

    result = f"{product}: {quantity} units available."

    print(f"[Tool Result] {result}")

    return result


# Tool: Search for an alternative product
def search_alternative(product: str) -> str:
    """Finds an alternative product with available stock."""

    print("\n[Tool Call] search_alternative")
    print(f"[Tool Arguments] product={product}")

    alternatives = {
        "laptop": "tablet",
        "tablet": "phone",
    }

    result = alternatives.get(
        product.lower(),
        "No alternative found."
    )

    print(f"[Tool Result] {result}")

    return result


# Configure the agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an inventory agent. "
        "Your goal is to find a product that is currently in stock. "
        "Continue checking products until the goal is achieved. "
        "Once an available product is found, stop and report the result."
    ),
    tools=[
        check_inventory,
        search_alternative,
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating goal-oriented agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Define the task
prompt = (
    "Find an available product starting with a laptop. "
    "The goal is to find a product with at least 1 unit in stock."
)

print("\n=== USER REQUEST ===")
print(prompt)


# Tell the agent about the goal
response = chat.send_message(
    f"""
Task:
{prompt}

Goal:
Find a product with at least 1 unit available.

Keep working until the goal is reached.
"""
)

step = 1
goal_completed = False

while not goal_completed:

    print(f"\n--- Agent Step {step} ---")

    if response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Action] {call.name}")
            print(f"[Arguments] {call.args}")

            if call.name == "check_inventory":

                result = check_inventory(**call.args)

                # Check the tool result for goal completion
                if "1 units" in result or "2 units" in result:
                    goal_completed = True

            elif call.name == "search_alternative":

                result = search_alternative(**call.args)

            else:

                result = "Unknown tool requested."

            # Send observation back to the agent
            response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            step += 1

    else:

        # No tool call means the model has stopped.
        break

    time.sleep(0.5)


print("\n=== GOAL STATUS ===")

if goal_completed:
    print("Goal completed: An available product was found.")
else:
    print("Goal not completed.")


print("\n=== FINAL AGENT RESPONSE ===")
print(response.text)
