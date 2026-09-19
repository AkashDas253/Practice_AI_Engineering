import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env from the local directory
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Specify model
model="models/gemini-3.5-flash-lite"


# Define sampling configuration parameters
config = types.GenerateContentConfig(
    temperature=0.7,
    top_p=0.9,
    top_k=40,
    stop_sequences=["END"]
)

print("Creating chat session with custom sampling parameters...")
chat = client.chats.create(model=model, config=config)

print("Sending generation request...")
response = chat.send_message("Write a short poem about solar power. Append the word 'END' at the finish.")

print("\n=== RESPONSE WITH CUSTOM PARAMETERS ===")
print(response.text)

time.sleep(3)