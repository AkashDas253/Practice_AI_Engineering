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

raw_support_ticket = """
User ID: 9482
Issue: Application crashes every time I export a PDF larger than 50MB on macOS Sonoma.
Workaround tried: Clearing cache did not help. Reinstalling app temporarily fixed it for 1 day.
"""

# Step 1: Fact Extraction
print("Executing Step 1: Fact Extraction...")
chat_step1 = client.chats.create(model=model)

step1_prompt = f"Extract key diagnostic facts (User ID, OS, Error Trigger, Workaround) as bullets:\n{raw_support_ticket}"
step1_response = chat_step1.send_message(step1_prompt)

extracted_facts = step1_response.text
print("=== STEP 1 EXTRACTION OUTPUT ===")
print(extracted_facts)

print("\nPausing ...")
time.sleep(0.5)

# Step 2: Recommendation Generation
print("Executing Step 2: Action Recommendation...")
chat_step2 = client.chats.create(model=model)

step2_prompt = f"Based ONLY on these support ticket facts, write a 2-sentence action recommendation for Tier 2:\n{extracted_facts}"
step2_response = chat_step2.send_message(step2_prompt)

print("=== STEP 2 RECOMMENDATION OUTPUT ===")
print(step2_response.text)