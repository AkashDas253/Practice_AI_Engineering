import asyncio
import warnings
from pathlib import Path
from dotenv import load_dotenv

# Suppress underlying SDK warnings for clean console output
warnings.filterwarnings("ignore")

from google.adk import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

from agent import root_agent

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

session_service = InMemorySessionService()
runner = Runner(
    agent=root_agent,
    app_name="basic_agent_app",
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
    user_id, session_id = "user_123", "session_001"

    await session_service.create_session(
        app_name="basic_agent_app",
        user_id=user_id,
        session_id=session_id
    )

    # 1. Pre-Sample Interaction
    print("--- Pre-Sample Interaction ---")
    pre_sample_prompt = "What is the main function of a default gateway?"
    print(f"User: {pre_sample_prompt}")
    await send_message(user_id, session_id, pre_sample_prompt)

    # 2. Interactive Loop
    print("--- Interactive Terminal Session Started ---")
    print("Type your message and press Enter (type 'exit' or 'quit' to stop).\n")

    while True:
        try:
            user_prompt = input("User: ").strip()
            
            if not user_prompt:
                continue
                
            if user_prompt.lower() in ("exit", "quit"):
                print("Exiting interactive session.")
                break

            await send_message(user_id, session_id, user_prompt)

        except (KeyboardInterrupt, EOFError):
            print("\nExiting session.")
            break

if __name__ == "__main__":
    asyncio.run(main())