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

# Tool 1: Inventory Lookup
def check_inventory(product_sku: str) -> str:
    """Checks warehouse stock levels for a given product SKU."""
    
    print(f"\n[Tool Call] check_inventory")
    print(f"[Tool Arguments] product_sku={product_sku}")

    inventory_db = {
        "SKU-101": "15 units available in Warehouse A",
        "SKU-202": "0 units available (Out of stock)",
    }

    result = inventory_db.get(
        product_sku,
        "Product SKU not found in system"
    )

    print(f"[Tool Result] {result}")

    return result

# Tool 2: Order Status Lookup
def get_order_status(order_id: int) -> str:
    """Retrieves shipping status for a customer order ID."""

    print(f"\n[Tool Call] get_order_status")
    print(f"[Tool Arguments] order_id={order_id}")

    orders_db = {
        9482: "Shipped via FedEx - Tracking #17294021 - Estimated Arrival: Tomorrow",
        3301: "Processing in distribution center",
    }

    result = orders_db.get(
        order_id,
        "Order ID not found"
    )

    print(f"[Tool Result] {result}")

    return result

config = types.GenerateContentConfig(
    tools=[check_inventory, get_order_status]
)

print("Creating chat session with multiple tools...")
chat = client.chats.create(model=model, config=config)

# Request 1: Triggers order status tool
print("\n--- Test 1: Order Status Intent ---")
res1 = chat.send_message("What is the current status of order #9482?")
print("Output:", res1.text)

time.sleep(0.5)

# Request 2: Triggers inventory lookup tool
print("\n--- Test 2: Inventory Intent ---")
res2 = chat.send_message("Do we have SKU-101 in stock right now?")
print("Output:", res2.text)

time.sleep(0.5)

# Request 3: No tool needed
print("\n--- Test 3: No Tool Intent ---")
res3 = chat.send_message("What is the capital of France?")
print("Output:", res3.text)

time.sleep(0.5)
