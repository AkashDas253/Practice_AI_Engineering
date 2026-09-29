import os
import time
import uuid
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

    weather = {
        "Tokyo": "Sunny, 72°F",
        "London": "Rainy, 58°F",
    }

    result = weather.get(
        location,
        "Weather data unavailable"
    )

    print(f"[Tool Result] {result}")

    return result


# Tool 2: Get exchange rate
def get_exchange_rate(
    from_currency: str,
    to_currency: str,
) -> str:
    """Gets an exchange rate between two currencies."""

    print("\n[Tool Call] get_exchange_rate")
    print(
        f"[Tool Arguments] "
        f"from={from_currency}, to={to_currency}"
    )

    rates = {
        ("USD", "JPY"): 155.0,
        ("USD", "EUR"): 0.92,
    }

    rate = rates.get(
        (from_currency.upper(), to_currency.upper()),
        None
    )

    if rate is None:
        result = "Exchange rate unavailable"
    else:
        result = (
            f"1 {from_currency.upper()} = "
            f"{rate} {to_currency.upper()}"
        )

    print(f"[Tool Result] {result}")

    return result


# Create a unique ID for each tool call
def create_call_id() -> str:
    return str(uuid.uuid4())


# Configure manual tool handling
config = types.GenerateContentConfig(
    tools=[get_weather, get_exchange_rate],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with tool-call correlation...")
chat = client.chats.create(model=model, config=config)


# Send request requiring multiple tools
prompt = (
    "What is the weather in Tokyo, and what is the "
    "exchange rate from USD to JPY?"
)

print(f"\n--- Test: Multiple Tool Calls ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Store tool results by call ID
tool_results = {}


# Process all requested tool calls
if response.function_calls:

    for call in response.function_calls:

        # Create an ID for this specific request
        call_id = create_call_id()

        print(f"\n[Tool Call ID] {call_id}")
        print(f"[Tool Name] {call.name}")
        print(f"[Tool Arguments] {call.args}")

        # Execute the requested tool
        if call.name == "get_weather":

            result = get_weather(**call.args)

        elif call.name == "get_exchange_rate":

            result = get_exchange_rate(**call.args)

        else:
            result = "Unknown tool requested."

        # Associate the result with the specific call
        tool_results[call_id] = {
            "tool_name": call.name,
            "result": result,
        }


# Display correlated results
print("\n=== CORRELATED TOOL RESULTS ===")

for call_id, data in tool_results.items():

    print(f"\n[Call ID] {call_id}")
    print(f"[Tool] {data['tool_name']}")
    print(f"[Result] {data['result']}")


# Return all tool results to the model
function_responses = []

for call_id, data in tool_results.items():

    function_responses.append(
        types.Part.from_function_response(
            name=data["tool_name"],
            response={
                "call_id": call_id,
                "result": data["result"],
            },
        )
    )


if function_responses:

    final_response = chat.send_message(function_responses)

    print("\n=== FINAL RESPONSE ===")
    print(final_response.text)

else:
    print("\nNo tool calls were requested.")
    print(response.text)

time.sleep(0.5)
