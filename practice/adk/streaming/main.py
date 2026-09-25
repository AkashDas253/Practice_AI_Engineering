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
    app_name="streaming_app",
    session_service=session_service
)


async def send_streaming_message(user_id: str, session_id: str, prompt_text: str):
    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt_text)]
    )

    print(f"\nUser: {prompt_text}")
    print("Agent (Streaming Live Tokens): ", end="", flush=True)

    event_count = 0

    # Stream event objects from ADK Runner
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        event_count += 1

        # Extract textual content parts from streaming generation events
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    # Print each incremental chunk immediately to the stdout buffer
                    print(part.text, end="", flush=True)

    print(f"\n\n[Debug Metadata] Total Streaming Events Processed: {event_count}\n")


async def main():
    user_id = "user_123"
    session_id = "session_001"

    await session_service.create_session(
        app_name="streaming_app",
        user_id=user_id,
        session_id=session_id
    )

    print("=== ADK Token & Event Streaming Demo ===")

    # Turn 1: Pre-seeded prompt designed to elicit streaming generation
    demo_prompt = "Explain how event loops and asynchronous I/O work in Python."
    await send_streaming_message(user_id, session_id, demo_prompt)

    # Interactive Loop
    print("-" * 50)
    print("=== Interactive Terminal Streaming Session ===")
    print("Type your message below (or 'exit'/'quit' to stop):\n")

    while True:
        try:
            user_input = input("User: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Session ended.")
                break

            await send_streaming_message(user_id, session_id, user_input)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    asyncio.run(main())