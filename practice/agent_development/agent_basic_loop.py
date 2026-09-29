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


# Define a simple tool
def get_weather(location: str) -> str:
    """Gets the current weather for a location."""

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


# Disable automatic tool execution so we can see the agent loop
config = types.GenerateContentConfig(
    tools=[get_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating basic agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Initial user request
prompt = "What is the weather in Tokyo?"
print(f"\n[User] {prompt}")

response = chat.send_message(prompt)

step = 1

# Basic agent loop
while True:

    print(f"\n--- Agent Step {step} ---")

    # Check whether the model requested a tool
    if response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Decision] Use tool: {call.name}")
            print(f"[Tool Arguments] {call.args}")

            # Execute the requested tool
            if call.name == "get_weather":

                tool_result = get_weather(**call.args)

                # Send the observation back to the model
                print("[Agent Observation] Sending tool result back to model...")

                response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": tool_result},
                    )
                )

                step += 1

    else:

        # No more actions are required
        print("\n[Agent Decision] No more actions required.")

        print("\n=== FINAL AGENT RESPONSE ===")
        print(response.text)

        break

    time.sleep(0.5)
