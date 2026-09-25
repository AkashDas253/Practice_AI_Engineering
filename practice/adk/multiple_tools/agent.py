from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from adk_practice/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

def calculate_tax(amount: float, rate: float = 0.18) -> str:
    """Calculates sales tax for a purchase order amount.

    Args:
        amount: The monetary value of the order in USD.
        rate: The tax percentage rate as a decimal (default is 0.18 for 18%).
    """
    tax = amount * rate
    total = amount + tax
    return f"Order Amount: ${amount:.2f} | Tax ({rate*100:.0f}%): ${tax:.2f} | Total:${total:.2f}"

def check_stock(item_name: str) -> str:
    """Checks inventory stock levels in the warehouse for a given product item.

    Args:
        item_name: Name of the product item (e.g., 'laptop', 'keyboard', 'mouse').
    """
    inventory = {
        "laptop": 12,
        "keyboard": 0,
        "mouse": 45,
        "monitor": 8
    }
    count = inventory.get(item_name.lower(), 0)
    if count > 0:
        return f"Item '{item_name}' is IN STOCK ({count} units available)."
    return f"Item '{item_name}' is OUT OF STOCK (0 units available)."

# Primary agent entry point for ADK CLI (`adk run multiple_tools`)
root_agent = Agent(
    name="multiple_tools_agent",
    model=MODEL_ID,
    instruction=(
        "You are an e-commerce assistant.\n"
        "Use `check_stock` for inventory queries and `calculate_tax` for order pricing calculations."
    ),
    tools=[calculate_tax, check_stock],
    description="Agent demonstrating dynamic tool selection across multiple registered Python functions."
)