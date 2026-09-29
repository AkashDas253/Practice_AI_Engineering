import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env sitting in the same folder as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"


def fetch_user_account_balance(user_id: int) -> str:
    """Fetches the account balance for a given numeric user ID."""
    print("\n[Tool Call] fetch_user_account_balance")
    print(f"[Tool Arguments] user_id={user_id}")

    # Simulated database
    database = {
        101: "$1,250.50",
        102: "$3,400.00",
    }

    try:
        if user_id <= 0:
            raise ValueError("Invalid User ID format. User ID must be a positive integer.")
        
        if user_id not in database:
            raise KeyError(f"User ID {user_id} was not found in the account database.")

        balance = database[user_id]
        result = f"Status: Success | User ID: {user_id} | Account Balance: {balance}"

    except Exception as e:
        # Return structured error details back to Gemini so it can inform the user gracefully
        result = f"Status: Error | Reason: {str(e)} | Suggestion: Please ask the user to verify their User ID."

    print(f"[Tool Result / Error Returned] {result}")
    return result


config = types.GenerateContentConfig(tools=[fetch_user_account_balance])

print("Creating chat session with tool error handling...")
chat = client.chats.create(model=model, config=config)

prompt = "Can you check the account balance for User ID 9999?"
print(f"Sending request for non-existent User ID:\n'{prompt}'")

response = chat.send_message(prompt)

print("\n=== TOOL ERROR HANDLING RESPONSE ===")
print(response.text)

time.sleep(3)