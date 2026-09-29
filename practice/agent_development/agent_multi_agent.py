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


# Specialist Agent 1: Weather
def get_weather(location: str) -> str:
    """Gets weather information for a location."""

    print("\n[Weather Agent Tool]")
    print(f"[Location] {location}")

    weather_data = {
        "Tokyo": "Sunny, 72°F",
        "London": "Rainy, 58°F",
        "Paris": "Cloudy, 64°F",
    }

    result = weather_data.get(
        location,
        "Weather information unavailable."
    )

    print(f"[Result] {result}")

    return result


# Specialist Agent 2: Attractions
def find_attractions(location: str) -> str:
    """Finds popular attractions in a location."""

    print("\n[Attractions Agent Tool]")
    print(f"[Location] {location}")

    attractions = {
        "Tokyo": "Shibuya Crossing, Tokyo Tower, Meiji Shrine",
        "London": "Big Ben, Tower Bridge, British Museum",
        "Paris": "Eiffel Tower, Louvre Museum, Notre-Dame",
    }

    result = attractions.get(
        location,
        "Attractions information unavailable."
    )

    print(f"[Result] {result}")

    return result


# Specialist Agent 3: Food
def find_food(location: str) -> str:
    """Finds food recommendations for a location."""

    print("\n[Food Agent Tool]")
    print(f"[Location] {location}")

    food_data = {
        "Tokyo": "Sushi, ramen, tempura",
        "London": "Fish and chips, pies, Sunday roast",
        "Paris": "Croissants, crepes, French cuisine",
    }

    result = food_data.get(
        location,
        "Food information unavailable."
    )

    print(f"[Result] {result}")

    return result


# Create Weather Agent
weather_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a weather specialist. "
        "Provide concise weather information."
    ),
    tools=[get_weather],
)

weather_agent = client.chats.create(
    model=model,
    config=weather_config,
)


# Create Attractions Agent
attractions_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a travel attractions specialist. "
        "Provide useful attraction information."
    ),
    tools=[find_attractions],
)

attractions_agent = client.chats.create(
    model=model,
    config=attractions_config,
)


# Create Food Agent
food_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a food specialist. "
        "Provide useful food recommendations."
    ),
    tools=[find_food],
)

food_agent = client.chats.create(
    model=model,
    config=food_config,
)


# Larger task
location = "Tokyo"

print("\n=== LARGER TASK ===")
print(f"Create a simple travel overview for {location}.")


# Ask each specialist to handle its part
print("\n=== WEATHER AGENT ===")

weather_response = weather_agent.send_message(
    f"Provide the weather information for {location}."
)

print(weather_response.text)


print("\n=== ATTRACTIONS AGENT ===")

attractions_response = attractions_agent.send_message(
    f"Provide the main attractions for {location}."
)

print(attractions_response.text)


print("\n=== FOOD AGENT ===")

food_response = food_agent.send_message(
    f"Provide some food recommendations for {location}."
)

print(food_response.text)


# Coordinator combines the specialist results
print("\n=== COORDINATOR ===")

coordinator_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a coordinator agent. "
        "Combine information from multiple specialist agents "
        "into one clear final response."
    )
)

coordinator_agent = client.chats.create(
    model=model,
    config=coordinator_config,
)


combined_information = f"""
Destination: {location}

Weather Specialist:
{weather_response.text}

Attractions Specialist:
{attractions_response.text}

Food Specialist:
{food_response.text}
"""

final_response = coordinator_agent.send_message(
    f"""
Create a concise travel overview using the specialist information below.

{combined_information}
"""
)

print("\n=== FINAL COORDINATED RESPONSE ===")
print(final_response.text)

time.sleep(0.5)
