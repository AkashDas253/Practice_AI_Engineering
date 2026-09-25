import asyncio
import warnings
from pathlib import Path
from dotenv import load_dotenv

warnings.filterwarnings("ignore")

# Load environment variables from the root .env file
env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="state_management_app",
    session_service=session_service
)


async def send_message(user_id: str, session_id: str, prompt_text: str):
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt_text)]
    )

    print("Agent: ", end="", flush=True)
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
    print("\n")


async def main():
    user_id = "user_123"
    session_id = "session_001"

    # Create session
    session = await session_service.create_session(
        app_name="state_management_app",
        user_id=user_id,
        session_id=session_id
    )

    # Inject pre-seeded initial state directly via session service
    session.state["user_name"] = "Alice"
    session.state["preferred_language"] = "Python"

    print("=== State Management Demo ===")
    print(f"Pre-seeded Session State: {dict(session.state)}\n")

    # Turn 1: Update session state dynamically via Tool call
    turn_1 = "Please set my preferred_theme setting to 'dark_mode' and timezone to 'UTC+5:30'."
    print(f"User: {turn_1}")
    await send_message(user_id, session_id, turn_1)

    # Turn 2: Retrieve and verify state
    turn_2 = "What settings do you currently have saved in my session state?"
    print(f"User: {turn_2}")
    await send_message(user_id, session_id, turn_2)

    # Interactive Loop
    print("-" * 50)
    print("=== Interactive Terminal Session ===")
    print("Type your message below (or 'exit'/'quit' to stop):\n")

    while True:
        try:
            user_input = input("User: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Session ended.")
                break

            await send_message(user_id, session_id, user_input)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    asyncio.run(main())