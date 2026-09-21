import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env file sitting in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

raw_query = "Write a python script to backup files."

# Phase 1: Meta-Prompt Optimization
print("Phase 1: Expanding raw query into engineered prompt...")
chat_meta = client.chats.create(model=model)

meta_prompt = f"""
You are a Prompt Engineering Expert.
Optimize this user query into a detailed prompt specifying error handling, logging, type hints, and CLI flags:
Query: '{raw_query}'

Output ONLY the final optimized prompt text.
"""

meta_res = chat_meta.send_message(meta_prompt)
optimized_prompt = meta_res.text

print("=== OPTIMIZED PROMPT ===")
print(optimized_prompt)

print("\nPausing ...")
time.sleep(.5)

# Phase 2: Final Execution
print("Phase 2: Generating final Python code using optimized prompt...")
chat_exec = client.chats.create(model=model)
final_res = chat_exec.send_message(optimized_prompt)

print("=== FINAL CODE OUTPUT ===")
print(final_res.text)