import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from dotenv import load_dotenv

from google.adk import Agent

# Load environment variables from parent directory .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"


def calculate_square_root(number: float) -> str:
    """Calculates the square root of a given positive number.

    Args:
        number: The numeric value to compute the square root for.
    """
    # Pre-execution Tool Callback Hook
    print(f"\n[Callback Log] 🛠️ BEFORE TOOL EXECUTION -> Executing 'calculate_square_root' with input: {number}")

    if number < 0:
        result = "Error: Cannot compute the square root of a negative number."
    else:
        result = f"The square root of {number} is {number ** 0.5}"

    # Post-execution Tool Callback Hook
    print(f"[Callback Log] ✅ AFTER TOOL EXECUTION -> Result: {result}")
    return result


# Standard Pydantic-compliant Agent declaration
root_agent = Agent(
    name="callback_demo_agent",
    model=MODEL_ID,
    instruction=(
        "You are an assistant designed to demonstrate lifecycle callbacks.\n"
        "Use the `calculate_square_root` tool whenever math or square root calculations are requested."
    ),
    tools=[calculate_square_root],
    description="Agent configured to test agent and tool execution lifecycle callbacks."
)