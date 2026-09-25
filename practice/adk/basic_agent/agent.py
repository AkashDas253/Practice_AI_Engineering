from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from adk_practice/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

root_agent = Agent(
    name="basic_agent",
    model=MODEL_ID,
    instruction=(
        "You are a network hardware expert.\n"
        "Rules:\n"
        "1. Limit your response to exactly two short bullet points.\n"
        "2. Do NOT mention any specific brand names, trademarks, or vendor models."
    ),
    description="Baseline ADK agent establishing model targeting and single-turn execution."
)