import os
import time
from pathlib import Path
from datetime import datetime

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


# Simple observability logger
def log_event(event: str, details: str = ""):
    timestamp = datetime.now().strftime("%H:%M:%S")

    print(
        f"[{timestamp}] "
        f"[OBSERVABILITY] "
        f"{event}"
        f"{' | ' + details if details else ''}"
    )


# Tool: Get product information
def get_product_price(product_id: int) -> str:
    """Gets the price of a product."""

    log_event(
        "TOOL_CALL",
        f"get_product_price(product_id={product_id})"
    )

    products = {
        101: 750.00,
        202: 1200.00,
    }

    if product_id not in products:
        log_event(
            "TOOL_ERROR",
            f"Product {product_id} not found"
        )
        raise ValueError("Product ID not found.")

    result = (
        f"Product {product_id} "
        f"costs ${products[product_id]:.2f}"
    )

    log_event(
        "TOOL_RESULT",
        result
    )

    return result


# Configure agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are a product assistant. "
        "Use the product tool when price information "
        "is required."
    ),
    tools=[get_product_price],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

log_event("AGENT_START")

chat = client.chats.create(
    model=model,
    config=config,
)

log_event(
    "AGENT_CREATED",
    f"model={model}"
)


# User request
prompt = "What is the price of product 101?"

log_event(
    "USER_INPUT",
    prompt
)


# Send request to agent
log_event(
    "MODEL_REQUEST",
    "Sending request to model"
)

response = chat.send_message(prompt)


# Inspect model response
if response.function_calls:

    log_event(
        "MODEL_DECISION",
        f"Requested {len(response.function_calls)} tool call(s)"
    )

    for call in response.function_calls:

        log_event(
            "TOOL_REQUEST",
            f"name={call.name}, args={call.args}"
        )

        try:

            # Execute requested tool
            result = get_product_price(
                product_id=int(
                    call.args["product_id"]
                )
            )

            log_event(
                "TOOL_EXECUTION_SUCCESS",
                f"name={call.name}"
            )


            # Send tool result back to model
            log_event(
                "FUNCTION_RESPONSE",
                f"Returning result for {call.name}"
            )

            final_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "result": result
                    },
                )
            )

            log_event(
                "MODEL_FINAL_RESPONSE",
                final_response.text
            )

            print("\n=== FINAL RESPONSE ===")
            print(final_response.text)

        except Exception as error:

            log_event(
                "TOOL_EXECUTION_ERROR",
                str(error)
            )

            error_response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={
                        "error": str(error)
                    },
                )
            )

            log_event(
                "MODEL_ERROR_RESPONSE",
                error_response.text
            )

            print("\n=== FINAL RESPONSE ===")
            print(error_response.text)

else:

    log_event(
        "MODEL_FINAL_RESPONSE",
        response.text
    )

    print("\n=== FINAL RESPONSE ===")
    print(response.text)


log_event("AGENT_END")

time.sleep(0.5)
