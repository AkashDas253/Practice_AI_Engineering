import os
import asyncio
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")


# ==== ASYNC GENERATION ====

async def main():

    print("\n==== SETUP CLIENT ====")

    client = genai.Client(api_key=api_key)

    model = "models/gemini-3.5-flash-lite"

    print(f"Model: {model}")


    # ==== SEND ASYNC REQUEST ====

    print("\n==== SENDING ASYNC REQUEST ====")

    prompt = "Explain what an API is in one sentence."

    print(f"Prompt: {prompt}")

    try:
        start_time = time.perf_counter()

        response = await client.aio.models.generate_content(
            model=model,
            contents=prompt,
        )

        elapsed = time.perf_counter() - start_time

    except Exception as e:
        print("\n==== ASYNC GENERATION ERROR ====")
        print(type(e).__name__)
        print(e)
        return


    # ==== RESPONSE ====

    print("\n==== ASYNC RESPONSE ====")
    print(response.text)


    # ==== RESPONSE DETAILS ====

    print("\n==== RESPONSE DETAILS ====")

    if response.candidates:
        candidate = response.candidates[0]
        print(f"Finish reason: {candidate.finish_reason}")

    print(f"Response time: {elapsed:.3f} seconds")


    # ==== TOKEN USAGE ====

    print("\n==== TOKEN USAGE ====")

    if response.usage_metadata:
        usage = response.usage_metadata

        print(f"Input tokens:  {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Total tokens:  {usage.total_token_count}")


    # ==== COMPLETE ====

    print("\n==== DEMO COMPLETE ====")


# ==== RUN ASYNC PROGRAM ====

asyncio.run(main())
