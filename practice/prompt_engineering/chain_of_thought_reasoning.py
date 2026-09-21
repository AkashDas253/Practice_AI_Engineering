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

prompt = """
Solve the following logic puzzle step-by-step.
First, write out your detailed reasoning inside <thinking>...</thinking> tags.
Then, output the final answer inside <answer>...</answer> tags.

Puzzle: A train leaves Station A at 60 mph. 30 minutes later, a second train leaves Station A on a parallel track at 80 mph. How many hours after the second train departs will it catch up to the first train?
"""

# Low temperature ensures deterministic math/logic reasoning
config = types.GenerateContentConfig(temperature=0.1)

print("Starting Chain-of-Thought reasoning session...")
chat = client.chats.create(model=model, config=config)

response = chat.send_message(prompt)

print("\n=== CHAIN-OF-THOUGHT RESPONSE ===")
print(response.text)

time.sleep(0.5)