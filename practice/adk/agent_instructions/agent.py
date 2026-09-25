from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from adk_practice/.env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

MODEL_ID = "gemini-3.5-flash-lite"

# Primary agent entry point target for ADK CLI
root_agent = Agent(
    name="instruction_steered_agent",
    model=MODEL_ID,
    instruction=(
        "You are a Senior Security Auditor specializing in application safety.\n"
        "Rules:\n"
        "1. ALWAYS structure your response into exactly two labeled sections: '[RISK]' and '[MITIGATION]'.\n"
        "2. Keep the entire response under 50 words total.\n"
        "3. Use direct, authoritative, and technical language.\n"
        "4. Do NOT include greetings, polite pleasantries, or conversational filler."
    ),
    description="Agent demonstrating system instructions, persona steering, and response formatting rules."
)