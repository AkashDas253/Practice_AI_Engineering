import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Environment configuration.

BASE_DIR = Path(__file__).resolve().parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env"
    )


# Gemini client.

client = genai.Client(
    api_key=api_key,
)


# AI model.

TODO_AGENT_MODEL = "gemini-3.5-flash-lite"

MAX_AGENT_STEPS = 10


# Observability configuration.

MAX_RUN_HISTORY = 500


# Reminder configuration.

REMINDER_CHECK_INTERVAL = 5
