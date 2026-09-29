import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field, ValidationError, field_validator
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


# Define tool argument validation rules
class TransferArguments(BaseModel):
    sender_id: int = Field(gt=0, description="Positive sender account ID")
    recipient_id: int = Field(gt=0, description="Positive recipient account ID")
    amount: float = Field(gt=0, description="Transfer amount")
    currency: str = Field(description="Currency code")

    @field_validator("currency")
    @classmethod
    def validate_currency(cls, value: str) -> str:
        value = value.upper()

        if value not in {"USD", "EUR", "GBP"}:
            raise ValueError(
                "Unsupported currency. Use USD, EUR, or GBP."
            )

        return value

    @field_validator("amount")
    @classmethod
    def validate_amount(cls, value: float) -> float:
        if value > 10000:
            raise ValueError(
                "Transfer amount cannot exceed 10,000."
            )

        return value


# Define tool
def transfer_funds(
    sender_id: int,
    recipient_id: int,
    amount: float,
    currency: str,
) -> str:
    """Transfers money between two user accounts."""

    print("\n[Tool Call] transfer_funds")
    print(
        f"[Tool Arguments] sender_id={sender_id}, "
        f"recipient_id={recipient_id}, "
        f"amount={amount}, currency={currency}"
    )

    result = (
        f"Successfully transferred {amount:.2f} {currency} "
        f"from account #{sender_id} to account #{recipient_id}."
    )

    print(f"[Tool Result] {result}")

    return result


# Validate arguments before executing the tool
def validate_and_execute(arguments: dict) -> str:
    print("\n[Validation]")
    print(f"[Raw Arguments] {arguments}")

    try:
        validated = TransferArguments.model_validate(arguments)

    except ValidationError as error:
        result = f"Tool execution rejected: {error}"
        print(f"[Validation Failed] {result}")
        return result

    print("[Validation Passed]")

    return transfer_funds(**validated.model_dump())


# Disable automatic tool execution
config = types.GenerateContentConfig(
    tools=[transfer_funds],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with argument validation...")
chat = client.chats.create(model=model, config=config)


# Send request requiring a tool
prompt = "Transfer 750 USD from account 101 to account 202."
print(f"\n--- Test: Valid Transfer ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Inspect tool call and validate its arguments
if response.function_calls:
    for call in response.function_calls:
        print(f"\n[Tool Request] {call.name}")
        print(f"[Model Arguments] {call.args}")

        if call.name == "transfer_funds":
            result = validate_and_execute(call.args)

            # Send validated tool result back to the model
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

else:
    print("\nNo tool call was requested.")
    print(response.text)

time.sleep(0.5)
