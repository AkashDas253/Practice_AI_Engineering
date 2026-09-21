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

chat = client.chats.create(model=model)

tot_prompt = """
Problem: A high-traffic web application experiences sudden memory spikes under heavy load.

Task: Use a Tree-of-Thoughts approach to solve this issue:
1. Branch 1 (Infrastructure & Memory Allocation): Analyze potential root causes at the OS/Container level.
2. Branch 2 (Application Code & Garbage Collection): Analyze potential root causes in memory leaks and GC patterns.
3. Branch 3 (Database & Connection Pooling): Analyze memory impact from unindexed queries and connection pool leaks.
4. Evaluation & Selection: Compare all 3 branches, rank them by probability, and select the best initial troubleshooting step.
"""

print("Executing Tree-of-Thought reasoning...")
response = chat.send_message(tot_prompt)

print("\n=== TREE-OF-THOUGHT ANALYSIS ===")
print(response.text)

time.sleep(.5)