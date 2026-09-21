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

# Initialize a multi-turn chat session
chat = client.chats.create(model=model)

# Turn 1: Generate initial draft
print("Turn 1: Requesting initial draft...")
draft_res = chat.send_message("Explain quantum computing in two sentences. Use a metaphor.")
print("=== INITIAL DRAFT ===")
print(draft_res.text)

print("\nPausing ...")
time.sleep(.5)

# Turn 2: Send critique rules in the same chat thread
critique_prompt = """
Review your previous response against these rules:
Rule 1: Exactly two sentences.
Rule 2: Must contain a clear real-world metaphor.
Rule 3: Must NOT use jargon like 'qubits' or 'superposition'.

List any violations, then output a final corrected version that passes all rules.
"""

print("Turn 2: Requesting self-critique and revision...")
correction_res = chat.send_message(critique_prompt)

print("=== SELF-CORRECTION OUTPUT ===")
print(correction_res.text)