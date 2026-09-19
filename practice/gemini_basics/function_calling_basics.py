import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# ==== SIMPLE FUNCTION ====

print("\n==== SIMPLE FUNCTION ====")


def get_current_weather(location: str) -> str:
    """Gets current weather condition for a city."""
    return f"The weather in {location} is 72°F and sunny."


config = types.GenerateContentConfig(
    tools=[get_current_weather]
)

chat = client.chats.create(
    model=model,
    config=config,
)

response = chat.send_message(
    "What is the weather like in Tokyo?"
)

print(response.text)


# ==== MULTIPLE FUNCTIONS ====

print("\n==== MULTIPLE FUNCTIONS ====")


def get_current_weather(location: str) -> str:
    """Gets current weather condition for a city."""
    return f"The weather in {location} is 72°F and sunny."


def get_time(location: str) -> str:
    """Gets the current time for a city."""
    return f"The current time in {location} is 10:30 AM."


config = types.GenerateContentConfig(
    tools=[
        get_current_weather,
        get_time,
    ]
)

chat = client.chats.create(
    model=model,
    config=config,
)

response = chat.send_message(
    "What is the weather and current time in Tokyo?"
)

print(response.text)


# ==== FUNCTION WITH MULTIPLE ARGUMENTS ====

print("\n==== FUNCTION WITH MULTIPLE ARGUMENTS ====")


def calculate_trip_cost(
    destination: str,
    days: int,
    people: int,
) -> str:
    """Calculates an estimated trip cost."""
    cost = days * people * 150
    return f"Estimated cost for {people} people visiting {destination} for {days} days: ${cost}."


config = types.GenerateContentConfig(
    tools=[calculate_trip_cost]
)

chat = client.chats.create(
    model=model,
    config=config,
)

response = chat.send_message(
    "Calculate the estimated cost for 2 people visiting Tokyo for 5 days."
)

print(response.text)


# ==== FUNCTION CALL DETAILS ====

print("\n==== FUNCTION CALL DETAILS ====")

response = client.models.generate_content(
    model=model,
    contents="What is the weather in Paris?",
    config=types.GenerateContentConfig(
        tools=[get_current_weather]
    ),
)

print("Text:")
print(response.text)

print("\nCandidates:")

if response.candidates:
    for candidate in response.candidates:
        print(candidate)


# ==== RAW RESPONSE ====

print("\n==== RAW RESPONSE ====")

print(json.dumps(
    response.model_dump(exclude_none=True),
    indent=2,
    default=str,
))
