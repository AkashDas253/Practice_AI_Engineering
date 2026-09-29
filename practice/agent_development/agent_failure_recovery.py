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


# Tool: Fetch product information
def get_product_price(product_id: int) -> str:
    """Gets the price of a product."""

    print("\n[Tool Call] get_product_price")
    print(f"[Tool Arguments] product_id={product_id}")

    # Simulate a temporary failure
    if product_id == 101:
        raise ConnectionError("Product service temporarily unavailable.")

    products = {
        202: 750.00,
        303: 1200.00,
    }

    if product_id not in products:
        raise ValueError("Product ID not found.")

    result = f"Product {product_id} costs ${products[product_id]:.2f}"

    print(f"[Tool Result] {result}")

    return result


# Configure agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an agent that retrieves product prices. "
        "If a tool fails, try to recover by retrying the operation. "
        "If recovery is not possible, report the failure clearly."
    ),
    tools=[get_product_price],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating failure-recovery agent...")
chat = client.chats.create(
    model=model,
    config=config,
)


# Request
prompt = "What is the price of product 101?"

print("\n=== USER REQUEST ===")
print(prompt)


# Ask the agent to perform the task
response = chat.send_message(prompt)

print("\n=== AGENT RESPONSE ===")

if response.function_calls:

    for call in response.function_calls:

        print(f"[Tool Request] {call.name}")
        print(f"[Arguments] {call.args}")


        # Try the tool
        try:

            result = get_product_price(
                product_id=int(call.args["product_id"])
            )

            print("\n[Execution Successful]")


            # Send successful result back to agent
            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

        except ConnectionError as error:

            # First failure
            print(f"\n[Tool Failure] {error}")
            print("[Recovery] Retrying tool...")


            # Retry once
            try:

                # Simulate recovery by using another product
                # or retrying the operation.
                result = get_product_price(
                    product_id=202
                )

                print("\n[Recovery Successful]")
                print(f"[Recovered Result] {result}")


                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={
                            "result": (
                                f"Original product lookup failed. "
                                f"Recovery lookup succeeded: {result}"
                            )
                        },
                    )
                )

                print("\n=== FINAL RESPONSE ===")
                print(final_response.text)

            except Exception as retry_error:

                print(f"\n[Recovery Failed] {retry_error}")

                final_response = chat.send_message(
                    types.Part.from_function_response(
                        name=call.name,
                        response={
                            "error": (
                                f"Tool failed and recovery failed: "
                                f"{retry_error}"
                            )
                        },
                    )
                )

                print("\n=== FINAL RESPONSE ===")
                print(final_response.text)

        except ValueError as error:

            # Non-recoverable failure
            print(f"\n[Tool Error] {error}")
            print("[Recovery] Cannot recover from this error.")

            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "error": str(error)
                    },
                )
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

else:

    print(response.text)


time.sleep(0.5)
