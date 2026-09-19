import os
import time
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load .env
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

# Specify model
model = "models/gemini-3.5-flash-lite"

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

print("Initializing chat session for real-time streaming...")
chat = client.chats.create(model=model)

print("\n=== STREAMED OUTPUT ===")

response_stream = chat.send_message_stream(
    "Explain cloud computing architecture in 3 short paragraphs."
)

chunks = []

# First: just display the response as it streams
for chunk in response_stream:
    chunks.append(chunk)
    print(chunk.text, end="", flush=True)

print("\n\nStream complete.")


# Analysis / details


print("\n=== RESPONSE ANALYSIS ===")

# Last chunk contains the final response metadata
final_chunk = chunks[-1]

print("\n--- Token Usage ---")

if final_chunk.usage_metadata:
    usage = final_chunk.usage_metadata

    print(f"Input tokens:  {usage.prompt_token_count}")
    print(f"Output tokens: {usage.candidates_token_count}")
    print(f"Total tokens:  {usage.total_token_count}")

print("\n--- Final Chunk JSON ---")

print(json.dumps(
    final_chunk.model_dump(exclude_none=True),
    indent=2,
    default=str
))

print("\n--- Chat History ---")

for message in chat.get_history():
    print(f"\nRole: {message.role}")

    for part in message.parts:
        if part.text:
            print(f"Text: {part.text}")

time.sleep(3)
