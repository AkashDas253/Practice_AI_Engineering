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


# Create the agent configuration
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a weather assistant. "
        "Use the available weather tool when weather information is needed."
    ),
    tools=[get_weather],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating agent with managed context...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Keep the context used by the application
context = {
    "user_name": "Alex",
    "preferred_unit": "Fahrenheit",
    "current_task": "Weather lookup",
}


def run_agent_turn(user_input: str):
    """Runs one agent turn using the current context."""

    print("\n================================")
    print("[USER INPUT]")
    print(user_input)

    # Build the context for this turn
    contextual_prompt = f"""
User: {context["user_name"]}
Preferred temperature unit: {context["preferred_unit"]}
Current task: {context["current_task"]}

User request:
{user_input}
"""

    print("\n[Context Sent To Agent]")
    print(contextual_prompt)

    response = chat.send_message(contextual_prompt)

    # Handle requested tools
    while response.function_calls:

        for call in response.function_calls:

            print(f"\n[Agent Decision] Use tool: {call.name}")
            print(f"[Tool Arguments] {call.args}")

            if call.name == "get_weather":

                tool_result = get_weather(**call.args)

                # Add the tool result to the current context
                context["last_tool_result"] = tool_result

                print("\n[Context Updated]")
                print(f"Last tool result: {context['last_tool_result']}")

                response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": tool_result},
                    )
                )

    print("\n[Agent Response]")
    print(response.text)


# Step 1
run_agent_turn("What is the weather in Tokyo?")

time.sleep(0.5)


# Change the context before the next step
context["preferred_unit"] = "Celsius"

print("\n[Application] Context changed: preferred unit = Celsius")


# Step 2
run_agent_turn("Now check the weather in London.")

time.sleep(0.5)


# Show the final context
print("\n================================")
print("=== FINAL APPLICATION CONTEXT ===")
print(context)
