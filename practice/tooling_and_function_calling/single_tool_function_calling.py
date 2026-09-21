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
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

# Define custom Python tool with type hints and docstring
def calculate_discount(original_price: float, discount_percent: float) -> str:
    """Calculates the final price after applying a percentage discount.
    
    Args:
        original_price: Original item price in USD.
        discount_percent: Percentage discount to apply (e.g. 20 for 20%).
    """
    savings = original_price * (discount_percent / 100.0)
    final_price = original_price - savings
    return f"Original: ${original_price:.2f}, Discount: {discount_percent}%, Final Price: ${final_price:.2f}"

config = types.GenerateContentConfig(tools=[calculate_discount])

print("Creating chat session with single tool binding...")
chat = client.chats.create(model=model, config=config)

print("Sending user request requiring calculation tool...")
response = chat.send_message("I want to buy a $250 jacket that is currently 15% off. How much will I pay?")

print("\n=== FINAL RESPONSE ===")
print(response.text)

time.sleep(.5)