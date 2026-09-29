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


# Specialist Agent 1: General support
def general_support(message: str) -> str:
    """Handles general customer support questions."""

    print("\n[General Support]")
    print(f"[Request] {message}")

    result = (
        "This request requires specialized billing assistance."
    )

    print(f"[Result] {result}")

    return result


# Specialist Agent 2: Billing
def billing_support(message: str) -> str:
    """Handles billing-related questions."""

    print("\n[Billing Support]")
    print(f"[Request] {message}")

    result = (
        "Billing support has reviewed the request. "
        "The customer's latest invoice is available for review."
    )

    print(f"[Result] {result}")

    return result


# Create the general support agent
general_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a general customer support agent. "
        "Handle simple questions yourself. "
        "If the request is related to billing, "
        "hand the task off to the billing specialist."
    ),
    tools=[general_support],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

general_agent = client.chats.create(
    model=model,
    config=general_config,
)


# Create the billing specialist agent
billing_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a billing specialist. "
        "Handle billing-related customer requests "
        "and provide a clear response."
    ),
    tools=[billing_support],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

billing_agent = client.chats.create(
    model=model,
    config=billing_config,
)


# Initial customer request
user_request = (
    "I was charged twice on my latest invoice. "
    "Can someone check this for me?"
)

print("\n=== USER REQUEST ===")
print(user_request)


# Send the request to the general agent
print("\n=== GENERAL AGENT ===")

response = general_agent.send_message(
    user_request
)

print(response.text)


# Demonstrate the handoff
print("\n=== HANDOFF ===")

handoff_prompt = f"""
The customer request requires billing assistance.

Original request:
{user_request}

Hand this request to the billing specialist.
Return the original request clearly so the specialist
has the information needed to continue.
"""

handoff_response = general_agent.send_message(
    handoff_prompt
)

print("[General Agent] Request handed off to Billing Agent.")
print(handoff_response.text)


# Pass the task to the billing specialist
print("\n=== BILLING AGENT ===")

billing_response = billing_agent.send_message(
    f"""
A task has been handed off to you by the general support agent.

Original customer request:
{user_request}

Please handle the request as the billing specialist.
"""
)

print(billing_response.text)


print("\n=== HANDOFF COMPLETE ===")
print("General Agent → Billing Agent → Final Response")

time.sleep(0.5)
