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

# Initialize Session Service and Runner
session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="sessions_app",
    session_service=session_service
)


async def send_message(user_id: str, session_id: str, prompt_text: str):
    """Encapsulates sending a turn and streaming the response."""
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

    # Create session state container
    await session_service.create_session(
        app_name="sessions_app",
        user_id=user_id,
        session_id=session_id
    )

    print("=== Multi-Turn History Persistence Demo ===")

    # Turn 1: Seed information into the session history
    turn_1 = "Hi! My name is Alice and my favorite framework is Google ADK."
    print(f"User: {turn_1}")
    await send_message(user_id, session_id, turn_1)

    # Turn 2: Query information to prove history is retained across turns
    turn_2 = "What is my name and what framework do I like?"
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