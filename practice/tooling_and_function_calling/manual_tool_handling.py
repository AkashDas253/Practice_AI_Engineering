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
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

def query_user_database(user_id: int) -> dict:
    """Fetches user metadata from backend database."""
    return {"user_id": user_id, "name": "Sarah Connor", "tier": "Enterprise"}

# Disable automatic tool execution
config = types.GenerateContentConfig(
    tools=[query_user_database],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

print("Creating chat session with Manual Function Calling (AFC disabled)...")
chat = client.chats.create(model=model, config=config)

print("Sending user request...")
response = chat.send_message("Fetch profile details for User ID 1024.")

# Inspect requested function calls
if response.function_calls:
    for call in response.function_calls:
        print(f"\n[Intercepted Function Call] Name: {call.name}")
        print(f"[Intercepted Arguments] {call.args}")
        
        # Manually execute local Python function
        if call.name == "query_user_database":
            uid = int(call.args.get("user_id", 0))
            result = query_user_database(uid)
            print(f"[Local Execution Result] {result}")
            
            time.sleep(.5)
            
            # Send result back manually as FunctionResponse
            final_res = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result}
                )
            )
            print("\n=== FINAL RESPONSE AFTER MANUAL TURN ===")
            print(final_res.text)

time.sleep(.5)