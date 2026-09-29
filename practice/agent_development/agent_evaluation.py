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


# Tool: Get product price
def get_product_price(product_id: int) -> str:
    """Gets the price of a product."""

    print("\n[Tool Call] get_product_price")
    print(f"[Tool Arguments] product_id={product_id}")

    products = {
        101: 750.00,
        202: 1200.00,
    }

    if product_id not in products:
        return "Product not found."

    result = (
        f"Product {product_id} costs "
        f"${products[product_id]:.2f}"
    )

    print(f"[Tool Result] {result}")

    return result


# Configure agent
agent_config = types.GenerateContentConfig(
    system_instruction=(
        "You are a product assistant. "
        "Use the product tool when price information "
        "is required. Give a clear final answer."
    ),
    tools=[get_product_price],
)

print("Creating agent...")
agent = client.chats.create(
    model=model,
    config=agent_config,
)


# Task given to the agent
task = "What is the price of product 101?"

print("\n=== TASK ===")
print(task)


# Run the agent
response = agent.send_message(task)

agent_result = response.text

print("\n=== AGENT RESULT ===")
print(agent_result)


# Evaluation criteria
criteria = [
    "The response mentions product 101.",
    "The response contains the correct price of $750.00.",
    "The response clearly answers the user's question.",
]


# Simple evaluator
def evaluate_agent_result(result: str) -> dict:
    """Evaluates the agent result against defined criteria."""

    print("\n=== EVALUATION ===")

    checks = {
        "mentions_product": "101" in result,
        "contains_correct_price": "750.00" in result,
        "answers_question": (
            "750" in result
            and len(result.strip()) > 0
        ),
    }

    passed = sum(checks.values())
    total = len(checks)

    print(
        f"[Evaluation Score] {passed}/{total}"
    )

    for name, passed_check in checks.items():
        status = "PASS" if passed_check else "FAIL"

        print(
            f"[{status}] {name}"
        )

    return {
        "checks": checks,
        "passed": passed,
        "total": total,
        "success": passed == total,
    }


# Evaluate the result
evaluation = evaluate_agent_result(
    agent_result
)


# Final evaluation summary
print("\n=== EVALUATION SUMMARY ===")

if evaluation["success"]:
    print("Agent task completed successfully.")
else:
    print("Agent task did not satisfy all criteria.")

print(
    f"Score: "
    f"{evaluation['passed']}/"
    f"{evaluation['total']}"
)

time.sleep(0.5)
