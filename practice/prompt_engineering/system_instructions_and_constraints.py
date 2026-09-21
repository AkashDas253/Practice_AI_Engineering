import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env file sitting in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

# Define system rules and negative constraints
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a network hardware expert.\n"
        "Rules:\n"
        "1. Limit your response to exactly two short bullet points.\n"
        "2. Do NOT mention any specific brand names, trademarks, or vendor models."
    )
)

print("Creating chat session with system constraints...")
chat = client.chats.create(model=model, config=config)

print("Sending prompt to Gemini...")
response = chat.send_message("How do I fix a home Wi-Fi router that continuously drops connections?")

print("\n=== RESPONSE WITH CONSTRAINTS ===")
print(response.text)

time.sleep(.5)