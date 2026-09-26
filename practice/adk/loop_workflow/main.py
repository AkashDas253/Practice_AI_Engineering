import asyncio
import time
import warnings
from pathlib import Path
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Load environment variables from root .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Import declared root_agent from agent.py
from agent import root_agent

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="loop_workflow_app",
    session_service=session_service
)

async def send_message(user_id: str, session_id: str, prompt_text: str, label: str = "User"):
    print(f"\n{label}: {prompt_text}")
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt_text)]
    )

    current_agent = None

    # Process streaming events and track active agents across loop iterations
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        event_author = (
            getattr(event, "author", None) 
            or getattr(event, "agent_name", None) 
            or "Workflow"
        )

        if event_author != current_agent:
            current_agent = event_author
            print(f"\n\n🤖 [Executing Agent: {current_agent}]")
            print("-" * 45)

        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
    print("\n")

async def main():
    user_id = "user_123"
    session_id = "session_001"

    await session_service.create_session(
        app_name="loop_workflow_app",
        user_id=user_id,
        session_id=session_id
    )

    # --- Step 1: Pre-entered Demo Turns ---
    print("=== Step 1: Pre-entered Demo Turns ===")
    
    await send_message(
        user_id, session_id,
        "Product: AI-Powered Smart Coffee Mug",
        label="Pre-entered Turn 1"
    )
    time.sleep(2)  # Delay for rate-limit protection

    await send_message(
        user_id, session_id,
        "Product: Ergonomic Standing Desk",
        label="Pre-entered Turn 2"
    )
    time.sleep(2)

    # --- Step 2: Interactive Terminal Session ---
    print("=" * 50)
    print("=== Step 2: Interactive Session ===")
    print("Type a product name to generate & refine a headline (or 'exit'/'quit' to stop):")

    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ("exit", "quit"):
                print("Ending session.")
                break

            await send_message(user_id, session_id, user_input, label="You")
            time.sleep(2)
        except (KeyboardInterrupt, EOFError):
            break

if __name__ == "__main__":
    asyncio.run(main())