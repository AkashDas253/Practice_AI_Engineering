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


# Configure the agent
config = types.GenerateContentConfig(
    tools=[get_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating stateful agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Keep simple application state
agent_state = {
    "last_location": None,
    "last_weather": None,
    "turn_count": 0,
}


def run_agent_turn(user_input: str):
    """Runs one agent turn while preserving state."""

    agent_state["turn_count"] += 1

    print(f"\n--- Agent Turn {agent_state['turn_count']} ---")
    print(f"[User] {user_input}")

    response = chat.send_message(user_input)

    while response.function_calls:

        for call in response.function_calls:

            print(f"[Agent Decision] Use tool: {call.name}")
            print(f"[Tool Arguments] {call.args}")

            if call.name == "get_weather":

                location = call.args["location"]

                # Update application state
                agent_state["last_location"] = location

                tool_result = get_weather(**call.args)

                # Update application state
                agent_state["last_weather"] = tool_result

                print("[Agent State Updated]")
                print(f"  Last Location: {agent_state['last_location']}")
                print(f"  Last Weather: {agent_state['last_weather']}")

                # Send observation back to the agent
                response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": tool_result},
                    )
                )

    print(f"\n[Agent Response] {response.text}")


# Turn 1
run_agent_turn("What is the weather in Tokyo?")

time.sleep(0.5)


# Turn 2
run_agent_turn("What was the last city we checked?")

time.sleep(0.5)


# Turn 3
run_agent_turn("What was the weather there?")

time.sleep(0.5)


print("\n=== FINAL AGENT STATE ===")
print(agent_state)
