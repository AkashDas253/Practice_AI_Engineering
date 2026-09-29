import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError
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


# Define expected tool result
class AccountBalanceResult(BaseModel):
    user_id: int = Field(gt=0)
    balance: float = Field(ge=0)
    currency: str
    status: str


# Define tool
def get_account_balance(user_id: int) -> dict:
    """Retrieves the account balance for a user."""

    print("\n[Tool Call] get_account_balance")
    print(f"[Tool Arguments] user_id={user_id}")

    result = {
        "user_id": user_id,
        "balance": 1250.50,
        "currency": "USD",
        "status": "success",
    }

    print(f"[Tool Result] {result}")

    return result


# Validate tool result before sending it to the model
def validate_tool_result(result: dict) -> dict:
    print("\n[Result Validation]")
    print(f"[Raw Result] {result}")

    try:
        validated = AccountBalanceResult.model_validate(result)

    except ValidationError as error:
        print(f"[Validation Failed] {error}")

        return {
            "status": "error",
            "message": "Tool returned an invalid result.",
        }

    print("[Validation Passed]")

    return validated.model_dump()


# Configure manual tool handling
config = types.GenerateContentConfig(
    tools=[get_account_balance],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with result validation...")
chat = client.chats.create(model=model, config=config)


# Send request requiring a tool
prompt = "What is the account balance for user 101?"
print(f"\n--- Test: Account Balance ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Inspect tool call
if response.function_calls:
    for call in response.function_calls:
        print(f"\n[Tool Request] {call.name}")
        print(f"[Model Arguments] {call.args}")

        if call.name == "get_account_balance":

            # Execute tool
            raw_result = get_account_balance(**call.args)

            # Validate result before sending it to the model
            validated_result = validate_tool_result(raw_result)

            # Send validated result back to the model
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response=validated_result,
                )
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

else:
    print("\nNo tool call was requested.")
    print(response.text)

time.sleep(0.5)
