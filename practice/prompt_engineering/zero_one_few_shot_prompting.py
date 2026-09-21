import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env file sitting in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Initialize Gemini Client
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

test_review = "The shipment arrived two days late, and the outer box was heavily damaged."

# Define prompt variations
zero_shot_prompt = f"Classify sentiment of: '{test_review}'"

one_shot_prompt = f"""
Classify sentiment using format: [CATEGORY] - Reason.
Review: Absolutely love this purchase!
Sentiment: [POSITIVE] - High satisfaction.

Review: {test_review}
Sentiment:
"""

few_shot_prompt = f"""
Classify sentiment using format: [CATEGORY] - Reason.
Review: Absolutely love this purchase!
Sentiment: [POSITIVE] - High satisfaction.

Review: Product broke after two days.
Sentiment: [NEGATIVE] - Short term failure.

Review: Average build quality, does what it claims.
Sentiment: [NEUTRAL] - Meets basic expectations.

Review: {test_review}
Sentiment:
"""

# 1. Zero-Shot Run
print("Sending Zero-Shot Request...")
chat = client.chats.create(model=model)
res_zero = chat.send_message(zero_shot_prompt)
print("=== ZERO-SHOT OUTPUT ===")
print(res_zero.text)

time.sleep(0.5)

# 2. One-Shot Run
print("\nSending One-Shot Request...")
chat = client.chats.create(model=model)
res_one = chat.send_message(one_shot_prompt)
print("=== ONE-SHOT OUTPUT ===")
print(res_one.text)

time.sleep(0.5)

# 3. Few-Shot Run
print("\nSending Few-Shot Request...")
chat = client.chats.create(model=model)
res_few = chat.send_message(few_shot_prompt)
print("=== FEW-SHOT OUTPUT ===")
print(res_few.text)