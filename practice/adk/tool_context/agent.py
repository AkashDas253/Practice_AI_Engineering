from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent
from google.adk.tools import ToolContext

# Load GEMINI_API_KEY from adk_practice/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

def get_user_permissions(tool_context: ToolContext) -> str:
    """Retrieves user profile role and permissions from the active runtime context."""
    user_id = getattr(tool_context, "user_id", "unknown_user")
    session_id = getattr(tool_context, "session_id", "unknown_session")

    mock_db = {
        "user_123": "Role: Senior Systems Engineer | Access Level: Admin [READ, WRITE, EXECUTE]",
        "user_456": "Role: Guest User | Access Level: Limited [READ_ONLY]"
    }
    
    details = mock_db.get(user_id, "User account not recognized in authorization database.")
    return f"Active Context Verified -> Session: '{session_id}' | User: '{user_id}' | {details}"

# Primary agent entry point for ADK CLI (`adk run tool_context`)
root_agent = Agent(
    name="tool_context_agent",
    model=MODEL_ID,
    instruction=(
        "You are an access control verification agent.\n"
        "Use the `get_user_permissions` tool whenever a user asks about their role, session, or system permissions."
    ),
    tools=[get_user_permissions],
    description="Agent demonstrating context-aware tool execution using ToolContext."
)