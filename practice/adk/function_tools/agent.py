from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from adk_practice/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

def check_device_status(device_id: str) -> str:
    """Checks the current operational status, CPU load, and health of a network device.

    Args:
        device_id: The identifier of the hardware device (e.g., 'router-01', 'switch-02').
    """
    inventory = {
        "router-01": "Status: ONLINE | CPU Load: 18% | Memory: 42% | Uptime: 14 days",
        "switch-02": "Status: WARNING | CPU Load: 92% | High Memory Usage | Packets Dropped: 140",
        "firewall-01": "Status: ONLINE | CPU Load: 11% | Active Sessions: 1,240",
    }
    return inventory.get(device_id.lower(), f"Device '{device_id}' was not found in the infrastructure database.")

# Primary agent entry point for ADK CLI (`adk run function_tools`)
root_agent = Agent(
    name="function_tools_agent",
    model=MODEL_ID,
    instruction=(
        "You are an IT infrastructure support agent.\n"
        "Use the `check_device_status` tool whenever a user asks about network device metrics or health."
    ),
    tools=[check_device_status],
    description="Agent demonstrating custom Python function tool registration and execution."
)