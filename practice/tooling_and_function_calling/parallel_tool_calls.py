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


def get_current_weather(location: str) -> str:
    """Gets current weather conditions for a given city location."""
    print("\n[Tool Call] get_current_weather")
    print(f"[Tool Arguments] location='{location}'")

    weather_db = {
        "Tokyo": "72°F and sunny",
        "London": "58°F and rainy",
        "New York": "65°F and cloudy",
    }
    result = f"Weather in {location}: {weather_db.get(location, '70°F and clear')}"

    print(f"[Tool Result] {result}")
    return result


def get_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Gets the exchange rate between two currency codes."""
    print("\n[Tool Call] get_exchange_rate")
    print(f"[Tool Arguments] from_currency='{from_currency}', to_currency='{to_currency}'")

    rates = {
        ("USD", "JPY"): 155.0,
        ("USD", "EUR"): 0.92,
        ("USD", "GBP"): 0.78,
    }
    rate = rates.get((from_currency.upper(), to_currency.upper()), 1.0)
    result = f"Exchange Rate: 1 {from_currency.upper()} = {rate} {to_currency.upper()}"

    print(f"[Tool Result] {result}")
    return result


config = types.GenerateContentConfig(tools=[get_current_weather, get_exchange_rate])

print("Creating chat session with parallel tool execution capabilities...")
chat = client.chats.create(model=model, config=config)

prompt = "What is the weather in Tokyo right now, and what is the exchange rate from USD to JPY?"
print(f"Sending prompt requiring multiple parallel tool calls:\n'{prompt}'")

response = chat.send_message(prompt)

print("\n=== PARALLEL TOOL CALLS RESPONSE ===")
print(response.text)

time.sleep(3)