from pathlib import Path
from dotenv import load_dotenv
from google.adk import Agent

# Load GEMINI_API_KEY from root .env
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

# Specify model
MODEL_ID = "gemini-3.5-flash-lite"

# Module-isolated output directory inside the artifacts/ folder
LOCAL_OUTPUT_DIR = Path(__file__).resolve().parent / "output"
LOCAL_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def save_artifact(filename: str, content: str) -> str:
    """Saves text content into the module's dedicated local output directory.

    Args:
        filename: Name of the output file (e.g., 'notes.txt', 'summary.md').
        content: Text content to write into the file.
    """
    output_path = LOCAL_OUTPUT_DIR / filename
    output_path.write_text(content, encoding="utf-8")
    return f"Artifact successfully created at 'artifacts/output/{filename}' ({len(content)} characters)."

def delete_artifact(filename: str) -> str:
    """Deletes a file artifact from the local output directory.

    Args:
        filename: Name of the artifact file to delete.
    """
    target_file = LOCAL_OUTPUT_DIR / filename
    if target_file.exists() and target_file.is_file():
        target_file.unlink()
        return f"Artifact '{filename}' successfully deleted."
    return f"Error: File '{filename}' not found in output directory."


def list_artifacts() -> str:
    """Lists all created artifact files in this module's local output folder."""
    files = [f.name for f in LOCAL_OUTPUT_DIR.glob("*") if f.is_file()]
    if not files:
        return "No artifacts currently exist in 'artifacts/output/'."
    return "Existing artifacts in 'artifacts/output/':\n" + "\n".join(f"- {f}" for f in files)


root_agent = Agent(
    name="artifact_manager_agent",
    model=MODEL_ID,
    instruction=(
        "You are an agent capable of generating and inspecting persistent file artifacts.\n"
        "Always use save_artifact to store reports or code into your local module output directory, "
        "and list_artifacts to check what files have been generated."
    ),
    tools=[save_artifact, list_artifacts, delete_artifact],
    description="Agent for managing file artifacts inside a dedicated module directory.",
)