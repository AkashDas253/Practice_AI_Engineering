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


# Tool 1: Get customer account
def get_customer_account(customer_id: int) -> str:
    """Retrieves the customer account information."""

    print("\n[Tool Call] get_customer_account")
    print(f"[Tool Arguments] customer_id={customer_id}")

    accounts = {
        101: "Customer 101 - Enterprise account",
        202: "Customer 202 - Standard account",
    }

    result = accounts.get(
        customer_id,
        "Customer account not found"
    )

    print(f"[Tool Result] {result}")

    return result


# Tool 2: Get account benefits
def get_account_benefits(account_type: str) -> str:
    """Retrieves benefits available for an account type."""

    print("\n[Tool Call] get_account_benefits")
    print(f"[Tool Arguments] account_type={account_type}")

    benefits = {
        "Enterprise": "Priority support, advanced analytics, and dedicated account manager",
        "Standard": "Email support and basic analytics",
    }

    result = benefits.get(
        account_type,
        "No benefits found for this account type"
    )

    print(f"[Tool Result] {result}")

    return result


# Configure tools with automatic execution disabled
config = types.GenerateContentConfig(
    tools=[
        get_customer_account,
        get_account_benefits,
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating chat session with sequential tool dependencies...")
chat = client.chats.create(model=model, config=config)


prompt = "Find customer 101 and tell me what benefits their account has."
print(f"\n--- Test: Dependent Tool Calls ---")
print(f"User: {prompt}")

response = chat.send_message(prompt)


# Process the first tool call
if response.function_calls:

    for call in response.function_calls:

        print(f"\n[Tool Request] {call.name}")
        print(f"[Model Arguments] {call.args}")

        if call.name == "get_customer_account":

            # Execute the first tool
            account_result = get_customer_account(
                **call.args
            )

            # Send the first result back to the model
            response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": account_result},
                )
            )

            # The model now has the result needed for the next tool
            if response.function_calls:

                for next_call in response.function_calls:

                    print(f"\n[Dependent Tool Request] {next_call.name}")
                    print(f"[Model Arguments] {next_call.args}")

                    if next_call.name == "get_account_benefits":

                        # Execute the second tool using the first result
                        benefits_result = get_account_benefits(
                            **next_call.args
                        )

                        # Send the second result back to the model
                        final_response = chat.send_message(
                            types.Part.from_function_response(
                                name=next_call.name,
                                response={"result": benefits_result},
                            )
                        )

                        print("\n=== FINAL RESPONSE ===")
                        print(final_response.text)

            else:
                print("\nNo dependent tool call was requested.")

else:
    print("\nNo tool call was requested.")
    print(response.text)

time.sleep(0.5)
