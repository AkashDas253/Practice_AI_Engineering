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

# Define Agent Tools
def convert_currency(amount: float, from_curr: str, to_curr: str) -> str:
    """Converts money between supported currencies."""

    print(f"\n[Tool Call] convert_currency")
    print(
        f"[Tool Arguments] amount={amount}, "
        f"from_curr={from_curr}, to_curr={to_curr}"
    )

    rates = {("USD", "EUR"): 0.92, ("EUR", "USD"): 1.09}

    key = (from_curr.upper(), to_curr.upper())

    if key not in rates:
        result = (
            f"Unsupported currency conversion: "
            f"{from_curr.upper()} -> {to_curr.upper()}"
        )
        print(f"[Tool Result] {result}")
        return result

    converted = amount * rates[key]

    result = (
        f"{amount} {from_curr.upper()} = "
        f"{converted:.2f} {to_curr.upper()}"
    )

    print(f"[Tool Result] {result}")

    return result


def calculate_tax(
    amount: float,
    tax_rate_percent: float,
    currency: str,
) -> str:
    """Calculates tax amount for a given monetary figure."""

    print(f"\n[Tool Call] calculate_tax")
    print(
        f"[Tool Arguments] amount={amount}, "
        f"tax_rate_percent={tax_rate_percent}, currency={currency}"
    )

    tax = amount * (tax_rate_percent / 100.0)

    result = (
        f"Tax ({tax_rate_percent}%): "
        f"{tax:.2f} {currency.upper()}, "
        f"Total with Tax: "
        f"{amount + tax:.2f} {currency.upper()}"
    )

    print(f"[Tool Result] {result}")

    return result


# Configure ReAct Agent behavior
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an AI Financial Agent. "
        "Break down complex math/currency tasks step-by-step. "
        "Use provided tools for calculations and state your final answer clearly."
    ),
    tools=[convert_currency, calculate_tax]
)

print("Starting ReAct Agent session...")
chat = client.chats.create(model=model, config=config)

# Turn 1: Multi-step request
print("\n--- Turn 1: Multi-Step Financial Task ---")
prompt1 = "I have 500 USD. Convert it to EUR, then calculate a 19% VAT tax on that converted EUR amount."
print(f"User: {prompt1}")

res1 = chat.send_message(prompt1)
print(f"Agent:\n{res1.text}")

time.sleep(.5)

# Turn 2: Follow-up relying on session context
print("\n--- Turn 2: Conversational Follow-Up ---")
prompt2 = "What was the final total in EUR including tax from our previous calculation?"
print(f"User: {prompt2}")

res2 = chat.send_message(prompt2)
print(f"Agent:\n{res2.text}")

time.sleep(.5)
