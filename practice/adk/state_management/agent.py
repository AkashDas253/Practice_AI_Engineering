import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from dotenv import load_dotenv

from google.adk import Agent
from google.adk.tools import ToolContext

# Load environment variables from parent directory .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"


def update_user_preference(key: str, value: str, tool_context: ToolContext) -> str:
    """Updates or sets a key-value preference in the user's active session state.

    Args:
        key: The state variable key name (e.g., 'theme', 'preferred_language', 'timezone').
        value: The string value to assign to the key.
        tool_context: Runtime tool context injected automatically by ADK.
    """
    # Write directly to session state
    tool_context.state[key] = value
    return f"Successfully saved session state: {key} = '{value}'"


def get_user_preferences(tool_context: ToolContext) -> str:
    """Retrieves all custom key-value preferences currently stored in the session state."""
    # Convert ADK State object to a standard Python dictionary
    state_dict = tool_context.state.to_dict() if hasattr(tool_context.state, "to_dict") else dict(tool_context.state)

    if not state_dict:
        return "No user preferences currently set in session state."

    formatted_items = [f"- {k}: {v}" for k, v in state_dict.items()]
    return "Current Session State Variables:\n" + "\n".join(formatted_items)


# Expose root_agent for ADK CLI (`adk run state_management`)
root_agent = Agent(
    name="state_management_agent",
    model=MODEL_ID,
    instruction=(
        "You are a state-aware personal assistant.\n"
        "1. Use `update_user_preference` to store key-value settings when requested by the user.\n"
        "2. Use `get_user_preferences` to fetch and review active session settings.\n"
        "3. Always check session state when making recommendations based on user preferences."
    ),
    tools=[update_user_preference, get_user_preferences],
    description="Agent demonstrating reading and writing runtime variables in session memory."
)