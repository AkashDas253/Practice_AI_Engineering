import warnings
warnings.filterwarnings("ignore")

from pathlib import Path
from dotenv import load_dotenv

from google.adk import Agent

# Load environment variables from parent directory .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

# Root agent configured for streaming demonstrations
root_agent = Agent(
    name="streaming_agent",
    model=MODEL_ID,
    instruction=(
        "You are an engaging technical storyteller and software architect.\n"
        "Explain complex technical topics in vivid detail using simple analogies.\n"
        "Provide thorough, multi-paragraph responses to allow clear demonstration of token streaming."
    ),
    description="Agent configured to demonstrate real-time response token streaming."
)