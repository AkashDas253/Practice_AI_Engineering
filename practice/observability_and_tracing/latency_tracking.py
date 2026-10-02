import logging
import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Config

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# Tool

def get_weather(city: str) -> dict:
    """Returns simulated weather information."""

    time.sleep(0.05)

    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        }
    }

    return weather_data.get(
        city,
        {
            "city": city,
            "temperature_c": 25,
            "condition": "Unknown",
        },
    )


# Measure one model call

def measure_model_latency(prompt: str) -> tuple[str, float]:

    start = time.perf_counter()

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    elapsed = time.perf_counter() - start

    return response.text.strip(), elapsed


# Measure one tool call

def measure_tool_latency(city: str) -> tuple[dict, float]:

    start = time.perf_counter()

    result = get_weather(city)

    elapsed = time.perf_counter() - start

    return result, elapsed


# Run example

def run_example() -> None:

    prompt = "What is Python?"

    total_start = time.perf_counter()

    logging.info("Application started")

    logging.info("Model request started")

    model_response, model_latency = measure_model_latency(prompt)

    logging.info(
        "Model request completed | latency=%.4f seconds",
        model_latency,
    )

    logging.info(
        "Model response | response=%s",
        model_response,
    )

    logging.info("Tool call started | tool=get_weather")

    weather_result, tool_latency = measure_tool_latency("Kolkata")

    logging.info(
        "Tool call completed | latency=%.4f seconds | result=%s",
        tool_latency,
        weather_result,
    )

    total_latency = time.perf_counter() - total_start

    logging.info(
        "End-to-end execution completed | latency=%.4f seconds",
        total_latency,
    )

    print("\n=== Latency Summary ===")
    print(f"Model latency:       {model_latency:.4f} seconds")
    print(f"Tool latency:        {tool_latency:.4f} seconds")
    print(f"End-to-end latency:  {total_latency:.4f} seconds")


run_example()
