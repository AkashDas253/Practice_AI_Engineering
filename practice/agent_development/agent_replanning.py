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


# Tool 1: Check hotel availability
def check_hotel_availability(city: str) -> str:
    """Checks whether a hotel is available in a city."""

    print("\n[Tool Call] check_hotel_availability")
    print(f"[Tool Arguments] city={city}")

    hotel_data = {
        "Tokyo": "No hotels available for the requested dates.",
        "Osaka": "Hotel available: Osaka Central Hotel - $120/night.",
        "Kyoto": "Hotel available: Kyoto Garden Hotel - $150/night.",
    }

    result = hotel_data.get(
        city,
        "Hotel availability data unavailable."
    )

    print(f"[Tool Result] {result}")

    return result


# Tool 2: Check alternative destination
def check_alternative_destination(city: str) -> str:
    """Checks whether an alternative destination is suitable."""

    print("\n[Tool Call] check_alternative_destination")
    print(f"[Tool Arguments] city={city}")

    alternatives = {
        "Osaka": "Osaka is a suitable alternative with available hotels.",
        "Kyoto": "Kyoto is a suitable alternative with available hotels.",
    }

    result = alternatives.get(
        city,
        "No suitable alternative found."
    )

    print(f"[Tool Result] {result}")

    return result


# Configure the agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a travel planning agent. "
        "Create a plan for the user's request. "
        "Execute the plan step-by-step. "
        "If a step fails or produces an unexpected result, "
        "update the plan and continue with a suitable alternative."
    ),
    tools=[
        check_hotel_availability,
        check_alternative_destination,
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating replanning agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# User task
prompt = (
    "Plan a trip to Tokyo. "
    "First check whether a hotel is available. "
    "If Tokyo is unavailable, find a suitable alternative destination."
)

print("\n=== USER REQUEST ===")
print(prompt)


# Create the initial plan
planning_prompt = f"""
Create a short numbered plan for this task.

Do not execute any tools yet.

Task:
{prompt}
"""

print("\n=== INITIAL PLAN ===")

plan_response = chat.send_message(planning_prompt)

print(plan_response.text)


# Execute the initial plan
execution_prompt = f"""
Execute the plan for this task.

Task:
{prompt}

If a tool result shows that the planned step cannot be completed,
do not simply stop. Reassess the situation and create an updated plan.
"""

print("\n=== EXECUTION ===")

response = chat.send_message(execution_prompt)

step = 1

while True:

    print(f"\n--- Agent Step {step} ---")

    if response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Action] {call.name}")
            print(f"[Arguments] {call.args}")

            if call.name == "check_hotel_availability":

                result = check_hotel_availability(**call.args)

            elif call.name == "check_alternative_destination":

                result = check_alternative_destination(**call.args)

            else:

                result = "Unknown tool requested."

            # Send the observation back to the agent
            response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            step += 1

    else:

        print("\n=== AGENT RESPONSE ===")
        print(response.text)

        break

    time.sleep(0.5)
