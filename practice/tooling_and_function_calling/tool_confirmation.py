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


def transfer_funds(sender_id: int, recipient_id: int, amount: float) -> str:
    """Executes a financial transfer between two user accounts. (Sensitive Action)"""
    print("\n[Tool Call Execution] transfer_funds")
    print(f"[Tool Arguments] sender_id={sender_id}, recipient_id={recipient_id}, amount=${amount:.2f}")

    result = f"Successfully transferred ${amount:.2f} from Account #{sender_id} to Account #{recipient_id}."
    print(f"[Tool Result] {result}")
    return result


# Disable automatic function calling to intercept and require human approval
config = types.GenerateContentConfig(
    tools=[transfer_funds],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True)
)

print("Creating chat session with human-in-the-loop tool confirmation...")
chat = client.chats.create(model=model, config=config)

prompt = "Please transfer $250.00 from my account (ID: 101) to recipient account (ID: 202)."
print(f"Sending prompt requiring sensitive tool execution:\n'{prompt}'")

response = chat.send_message(prompt)

# Intercept tool call requests before execution
if response.function_calls:
    for call in response.function_calls:
        print(f"\n[Intercepted Function Request] Name: {call.name}")
        print(f"[Requested Parameters] {call.args}")

        if call.name == "transfer_funds":
            sender_id = int(call.args.get("sender_id", 0))
            recipient_id = int(call.args.get("recipient_id", 0))
            amount = float(call.args.get("amount", 0.0))

            print("\n⚠️  HUMAN APPROVAL REQUIRED ⚠️")
            print(f"Pending Action: Transfer ${amount:.2f} from User #{sender_id} to User #{recipient_id}")
            
            # Real interactive CLI confirmation prompt
            user_decision = input("Do you approve this transaction? (yes/no): ").strip().lower()

            if user_decision in ["yes", "y"]:
                # Execute tool locally only after human confirmation
                execution_result = transfer_funds(sender_id, recipient_id, amount)

                time.sleep(1)

                # Send function execution response back to Gemini
                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"result": execution_result}
                    )
                )

                print("\n=== RESPONSE AFTER HUMAN APPROVAL ===")
                print(final_response.text)
            else:
                print("\n[Action Cancelled] Financial transfer was rejected by human operator.")
                rejection_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={"error": "User rejected the transaction. Transfer was not completed."}
                    )
                )

                print("\n=== RESPONSE AFTER REJECTION ===")
                print(rejection_response.text)

time.sleep(3)