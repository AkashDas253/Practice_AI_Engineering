import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

# Specify model
model = "models/gemini-3.5-flash-lite"

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

# Create Gemini client
client = genai.Client(api_key=api_key)

# Text to count
prompt = """
Explain prompt engineering to a beginner.
Give three practical examples.
"""

# Count input tokens
response = client.models.count_tokens(
    model=model,
    contents=prompt,
)

print("=== TOKEN COUNT ===")
print(f"Model: {model}")
print(f"Input tokens: {response.total_tokens}")
print(f"Characters: {len(prompt)}")
print(f"Words: {len(prompt.split())}")
print(f"Lines: {len(prompt.strip().splitlines())}")
