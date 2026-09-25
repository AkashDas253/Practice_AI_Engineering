import warnings
warnings.filterwarnings("ignore")

from google.adk import Agent

# Define the root agent for session history management
root_agent = Agent(
    name="session_assistant",
    model="gemini-3.5-flash-lite",
    instruction=(
        "You are a helpful, context-aware AI assistant. "
        "Maintain absolute consistency across multi-turn interactions. "
        "Refer back to details shared by the user in previous turns when relevant."
    ),
    description="An agent configured for multi-turn session persistence testing."
)