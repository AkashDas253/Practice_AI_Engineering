import json
from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from root .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Specify model 
MODEL_ID = "gemini-3.5-flash-lite"

# Module-isolated output directory inside memory/ folder
LOCAL_OUTPUT_DIR = Path(__file__).resolve().parent / "output"
LOCAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
MEMORY_FILE = LOCAL_OUTPUT_DIR / "memory_store.json"


def _load_memory_store() -> dict:
    if MEMORY_FILE.exists():
        try:
            return json.loads(MEMORY_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _save_memory_store(store: dict) -> None:
    MEMORY_FILE.write_text(json.dumps(store, indent=2), encoding="utf-8")


def store_memory(key: str, value: str) -> str:
    """Stores a fact, preference, or piece of knowledge into persistent memory.

    Args:
        key: The category, topic, or label (e.g., 'favorite_language', 'user_role').
        value: The detailed information to remember.
    """
    store = _load_memory_store()
    store[key.lower().strip()] = value.strip()
    _save_memory_store(store)
    return f"Successfully saved to memory: [{key.lower().strip()}] -> '{value.strip()}'"


def recall_memory(key: str) -> str:
    """Retrieves a previously stored memory or user fact by key.

    Args:
        key: The key or category to look up.
    """
    store = _load_memory_store()
    normalized_key = key.lower().strip()
    value = store.get(normalized_key)
    if value:
        return f"Retrieved Memory [{normalized_key}]: {value}"
    return f"No memory found for key '{normalized_key}'. Stored keys: {list(store.keys())}"


def list_memories() -> str:
    """Lists all stored memory keys and their values."""
    store = _load_memory_store()
    if not store:
        return "Memory store is currently empty."
    formatted = "\n".join(f"- {k}: {v}" for k, v in store.items())
    return f"All Stored Memories:\n{formatted}"


root_agent = Agent(
    name="memory_agent",
    model=MODEL_ID,
    instruction=(
        "You are an assistant with persistent memory storage capabilities.\n"
        "Use `store_memory` when the user asks you to remember facts or preferences.\n"
        "Use `recall_memory` or `list_memories` when retrieving past stored knowledge."
    ),
    tools=[store_memory, recall_memory, list_memories],
    description="Agent for semantic memory storage and retrieval across turns.",
)
