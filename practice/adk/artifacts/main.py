import asyncio
import warnings
from pathlib import Path
from dotenv import load_dotenv

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
    app_name="artifacts_app",
    session_service=session_service,
)


async def execute_turn(user_id: str, session_id: str, prompt: str):
    print(f"\n[User]: {prompt}\n")
    user_content = types.Content(
        role="user", parts=[types.Part.from_text(text=prompt)]
    )

    print("[Agent Response]:")
    async for event in runner.run_async(
        user_id=user_id, session_id=session_id, new_message=user_content
    ):
        if hasattr(event, "content") and event.content and event.content.parts:
            for part in event.content.parts:
                if part.text:
                    print(part.text, end="", flush=True)
    print("\n" + "-" * 60)


async def main():
    user_id = "user_001"
    session_id = "artifacts_session"

    await session_service.create_session(
        app_name="artifacts_app", user_id=user_id, session_id=session_id
    )

    # 1. Automated Example Interaction
    print("==================================================")
    print("         AUTOMATED EXAMPLE INTERACTION            ")
    print("==================================================")
    example_prompt = "Generate a quick cheat sheet on Python list comprehensions and save it as 'list_comp_cheatsheet.md'."
    await execute_turn(user_id, session_id, example_prompt)

    # 2. Interactive User Input Session
    print("\n==================================================")
    print("   INTERACTIVE SESSION (Type 'exit' to quit)     ")
    print("==================================================")
    while True:
        try:
            user_input = input("\nYou: ").strip()
            if not user_input:
                continue
            if user_input.lower() in ["exit", "quit"]:
                print("Ending session.")
                break
            await execute_turn(user_id, session_id, user_input)
        except (KeyboardInterrupt, EOFError):
            print("\nEnding session.")
            break


if __name__ == "__main__":
    asyncio.run(main())