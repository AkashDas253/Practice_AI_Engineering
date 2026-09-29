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


# Define tool
def delete_user_account(user_id: int) -> str:
    """Deletes a user account."""

    print("\n[Tool Call] delete_user_account")
    print(f"[Tool Arguments] user_id={user_id}")

    result = f"User account #{user_id} has been deleted."

    print(f"[Tool Result] {result}")

    return result


# Check whether the current user is authorized
def is_authorized(user_id: int, current_user_role: str) -> bool:

    print("\n[Authorization Check]")
    print(f"[Current User Role] {current_user_role}")
    print(f"[Requested User ID] {user_id}")

    allowed_roles = {"admin"}

    if current_user_role in allowed_roles:
        print("[Authorization Passed]")
        return True

    print("[Authorization Failed]")
    return False


# Disable automatic tool execution
config = types.GenerateContentConfig(
    tools=[delete_user_account],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with authorization check...")
chat = client.chats.create(model=model, config=config)


# Simulate the current application user
current_user_role = "admin"

prompt = "Delete user account 1024."
print(f"\n--- Test: Account Deletion ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Inspect tool call
if response.function_calls:
    for call in response.function_calls:

        print(f"\n[Tool Request] {call.name}")
        print(f"[Model Arguments] {call.args}")

        if call.name == "delete_user_account":

            user_id = int(call.args["user_id"])

            # Check authorization before executing the tool
            if is_authorized(user_id, current_user_role):

                # Execute tool only after authorization
                result = delete_user_account(user_id)

                # Send tool result back to the model
                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": result},
                    )
                )

                print("\n=== FINAL RESPONSE ===")
                print(final_response.text)

            else:
                # Do not execute the tool when authorization fails
                result = "Authorization failed. The account was not deleted."

                print(f"\n[Action Blocked] {result}")

                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"error": result},
                    )
                )

                print("\n=== FINAL RESPONSE ===")
                print(final_response.text)

else:
    print("\nNo tool call was requested.")
    print(response.text)

time.sleep(0.5)
