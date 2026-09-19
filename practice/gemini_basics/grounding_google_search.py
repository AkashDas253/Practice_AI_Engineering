import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# ==== GOOGLE SEARCH ====

print("\n==== GOOGLE SEARCH ====")

config = types.GenerateContentConfig(
    tools=[
        types.Tool(
            google_search=types.GoogleSearch()
        )
    ]
)

chat = client.chats.create(
    model=model,
    config=config,
)

prompt = "What are the latest tech announcements from Google this month?"

try:
    response = chat.send_message(prompt)

    print("\n==== SEARCH-GROUNDED RESPONSE ====")
    print(response.text)

    print("\n==== RESPONSE DETAILS ====")

    if response.candidates:
        candidate = response.candidates[0]
        print(f"Finish reason: {candidate.finish_reason}")

    print("\n==== TOKEN USAGE ====")

    if response.usage_metadata:
        usage = response.usage_metadata

        print(f"Input tokens:  {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Total tokens:  {usage.total_token_count}")

except Exception as e:
    print("\n==== SEARCH ERROR ====")
    print(type(e).__name__)
    print(e)
