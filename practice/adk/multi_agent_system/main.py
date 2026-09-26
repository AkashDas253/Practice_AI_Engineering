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

# Import declared root_agent target
from agent import root_agent

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="multi_agent_app",
    session_service=session_service
)

async def send_message(user_id: str, session_id: str, prompt_text: str, label: str = "User"):
    print(f"\n{label}: {prompt_text}")
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt_text)]
    )

    current_agent = None

    # Process events and track dynamically active agents
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
        app_name="multi_agent_app",
        user_id=user_id,
        session_id=session_id
    )

    # --- Step 1: Pre-entered Demo Turns ---
    print("=== Step 1: Pre-entered Demo Turns ===")

    # Turn 1: Billing Query
    await send_message(
        user_id, session_id,
        "I noticed a duplicate charge on my last invoice. How can I get a refund?",
        label="Pre-entered Turn 1"
    )
    time.sleep(2)

    # Turn 2: Technical Query
    await send_message(
        user_id, session_id,
        "My app crashed with HTTP error 500 while trying to fetch the user profile API.",
        label="Pre-entered Turn 2"
    )
    time.sleep(2)

    # Turn 3: Creative Query
    await send_message(
        user_id, session_id,
        "Can you write a catchy 1-line slogan for our new solar power technology startup?",
        label="Pre-entered Turn 3"
    )
    time.sleep(2)

    # --- Step 2: Interactive Terminal Session ---
    print("=" * 50)
    print("=== Step 2: Interactive Session ===")
    print("Ask a query to test dynamic routing (or 'exit'/'quit' to stop):")

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