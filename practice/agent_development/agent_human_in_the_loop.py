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


# Tool: Create an order
def create_order(product: str, quantity: int) -> str:
    """Creates an order for a product."""

    print("\n[Tool Call] create_order")
    print(f"[Tool Arguments] product={product}, quantity={quantity}")

    result = (
        f"Order created successfully: "
        f"{quantity} x {product}"
    )

    print(f"[Tool Result] {result}")

    return result


# Configure agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an order assistant. "
        "When an order needs to be created, request the tool. "
        "The application will require human approval before "
        "the tool is executed."
    ),
    tools=[create_order],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating Human-in-the-Loop Agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# User request
prompt = "Create an order for 3 keyboards."

print("\n=== USER REQUEST ===")
print(prompt)


# Ask the agent to process the request
response = chat.send_message(prompt)


# Inspect the requested action
if response.function_calls:

    for call in response.function_calls:

        print("\n=== AGENT REQUESTED ACTION ===")
        print(f"Tool: {call.name}")
        print(f"Arguments: {call.args}")


        # Pause for human approval
        print("\n=== HUMAN APPROVAL REQUIRED ===")

        decision = input(
            "Do you approve this action? (yes/no): "
        ).strip().lower()


        if decision in ["yes", "y"]:

            print("\n[Human Approved]")

            # Execute tool only after approval
            result = create_order(
                product=call.args["product"],
                quantity=int(call.args["quantity"]),
            )

            # Send result back to agent
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            print("\n=== FINAL AGENT RESPONSE ===")
            print(final_response.text)

        else:

            print("\n[Human Rejected]")

            # Tell the agent the action was rejected
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "error": (
                            "The human operator rejected "
                            "the requested action."
                        )
                    },
                )
            )

            print("\n=== FINAL AGENT RESPONSE ===")
            print(final_response.text)

else:

    print("\nNo tool action was requested.")
    print(response.text)


time.sleep(0.5)
