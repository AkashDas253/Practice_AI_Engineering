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
    app_name="callbacks_app",
    session_service=session_service
)


async def run_with_callbacks(user_id: str, session_id: str, prompt_text: str):
    """Execution harness providing before/after lifecycle hooks for agents and models."""
    
    # 1. BEFORE AGENT RUN HOOK
    print("\n[Callback Log] 🚀 BEFORE AGENT RUN -> Preparing message payload.")

    user_content = types.Content(
        role="user",
        parts=[types.Part.from_text(text=prompt_text)]
    )

    print(f"User: {prompt_text}")
    
    # 2. BEFORE MODEL CALL HOOK
    print("[Callback Log] 🧠 BEFORE MODEL CALL -> Invoking Gemini LLM stream.")
    print("Agent Response: ", end="", flush=True)

    event_count = 0
    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=user_content
    ):
        event_count += 1
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)

    # 3. AFTER MODEL CALL HOOK
    print(f"\n[Callback Log] 📥 AFTER MODEL CALL -> Streaming turn finished ({event_count} events processed).")

    # 4. AFTER AGENT RUN HOOK
    print("[Callback Log] 🏁 AFTER AGENT RUN -> Agent turn completed successfully.\n")


async def main():
    user_id = "user_123"
    session_id = "session_001"

    await session_service.create_session(
        app_name="callbacks_app",
        user_id=user_id,
        session_id=session_id
    )

    print("=== ADK Execution Lifecycle Callbacks Demo ===")

    # Turn 1: Triggers agent, model, and tool callbacks
    turn_1 = "Please calculate the square root of 256 for me."
    await run_with_callbacks(user_id, session_id, turn_1)

    # Interactive Loop
    print("-" * 50)
    print("=== Interactive Terminal Session with Callbacks ===")
    print("Type your message below (or 'exit'/'quit' to stop):\n")

    while True:
        try:
            user_input = input("User: ").strip()

            if not user_input:
                continue

            if user_input.lower() in ("exit", "quit"):
                print("Session ended.")
                break

            await run_with_callbacks(user_id, session_id, user_input)

        except (KeyboardInterrupt, EOFError):
            print("\nSession ended.")
            break


if __name__ == "__main__":
    asyncio.run(main())