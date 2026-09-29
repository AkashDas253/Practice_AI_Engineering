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


# Tool 1: Get weather
def get_weather(location: str) -> str:
    """Gets the weather for a location."""

    print("\n[Tool Call] get_weather")
    print(f"[Tool Arguments] location={location}")

    weather_data = {
        "Tokyo": "Sunny, 72°F",
        "London": "Rainy, 58°F",
        "New York": "Cloudy, 65°F",
    }

    result = weather_data.get(
        location,
        "Weather data unavailable"
    )

    print(f"[Tool Result] {result}")

    return result


# Tool 2: Get travel recommendation
def get_travel_recommendation(
    destination: str,
    weather: str,
) -> str:
    """Provides a simple travel recommendation based on weather."""

    print("\n[Tool Call] get_travel_recommendation")
    print(
        f"[Tool Arguments] "
        f"destination={destination}, weather={weather}"
    )

    if "Sunny" in weather:
        result = f"{destination} is a good choice for outdoor activities."
    elif "Rainy" in weather:
        result = f"{destination} may require an umbrella and indoor activities."
    else:
        result = f"{destination} has moderate conditions for travel."

    print(f"[Tool Result] {result}")

    return result


# Configure the agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a travel planning agent. "
        "For complex requests, first create a clear plan with ordered steps. "
        "Then execute the steps using the available tools."
    ),
    tools=[
        get_weather,
        get_travel_recommendation,
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating planning agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Complex task
prompt = (
    "Help me decide whether Tokyo is a good destination for outdoor "
    "activities. Check the weather first, then make a recommendation."
)

print("\n=== USER REQUEST ===")
print(prompt)


# Ask the model to create a plan first
planning_prompt = f"""
Create a short numbered plan for this task.

Do not execute any tools yet.

Task:
{prompt}
"""

print("\n=== PLANNING ===")

plan_response = chat.send_message(planning_prompt)

print(plan_response.text)


# Tell the agent to execute the plan
execution_prompt = f"""
Now execute the plan you created.

Task:
{prompt}

Use the available tools where appropriate.
Follow the planned steps in order.
"""

print("\n=== EXECUTION ===")

response = chat.send_message(execution_prompt)

step = 1

# Execute the planned tool calls
while True:

    print(f"\n--- Execution Step {step} ---")

    if response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Action] {call.name}")
            print(f"[Arguments] {call.args}")

            if call.name == "get_weather":

                result = get_weather(**call.args)

            elif call.name == "get_travel_recommendation":

                result = get_travel_recommendation(**call.args)

            else:

                result = "Unknown tool requested."

            # Send tool result back to the agent
            response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            step += 1

    else:

        print("\n=== FINAL RESPONSE ===")
        print(response.text)

        break

    time.sleep(0.5)
