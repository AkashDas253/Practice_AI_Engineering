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

client = genai.Client(api_key=api_key)

# Create a chat session
chat = client.chats.create(model=model)

print("=== Message 1 ===")
response = chat.send_message(
    "My favorite programming language is Python."
)
print(response.text)

print("\n=== Message 2 ===")
response = chat.send_message(
    "What programming language did I say I like?"
)
print(response.text)


# Chat history

print("\n=== Chat History ===")

history = chat.get_history()

for i, message in enumerate(history, 1):
    print(f"\n--- Message {i} ---")
    print(f"Role: {message.role}")
    print(f"Parts: {len(message.parts)}")

    for j, part in enumerate(message.parts, 1):
        print(f"  Part {j}:")
        print(f"    Text: {part.text}")
