import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Config

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# Track one model request

def run_request(prompt: str) -> None:

    logging.info(
        "Model request started | prompt=%s",
        prompt,
    )

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    usage = response.usage_metadata

    prompt_tokens = usage.prompt_token_count or 0
    output_tokens = usage.candidates_token_count or 0
    total_tokens = usage.total_token_count or 0

    logging.info(
        "Model request completed | prompt_tokens=%s | output_tokens=%s | total_tokens=%s",
        prompt_tokens,
        output_tokens,
        total_tokens,
    )

    print("\n=== Request ===")
    print(f"Prompt: {prompt}")

    print("\n=== Response ===")
    print(response.text.strip())

    print("\n=== Token Usage ===")
    print(f"Prompt tokens:  {prompt_tokens}")
    print(f"Output tokens:  {output_tokens}")
    print(f"Total tokens:   {total_tokens}")


# Track token usage across a conversation

def run_conversation() -> None:

    chat = client.chats.create(model=model)

    prompts = [
        "What is Python? Answer in one sentence.",
        "What is it commonly used for? Answer in one sentence.",
    ]

    total_prompt_tokens = 0
    total_output_tokens = 0
    total_tokens = 0

    print("\n=== Conversation Token Usage ===")

    for index, prompt in enumerate(prompts, start=1):

        logging.info(
            "Conversation request started | turn=%s",
            index,
        )

        response = chat.send_message(prompt)

        usage = response.usage_metadata

        prompt_tokens = usage.prompt_token_count or 0
        output_tokens = usage.candidates_token_count or 0
        request_total = usage.total_token_count or 0

        total_prompt_tokens += prompt_tokens
        total_output_tokens += output_tokens
        total_tokens += request_total

        print(f"\n--- Turn {index} ---")
        print(f"Prompt: {prompt}")
        print(f"Response: {response.text.strip()}")
        print(f"Prompt tokens: {prompt_tokens}")
        print(f"Output tokens: {output_tokens}")
        print(f"Total tokens: {request_total}")

        logging.info(
            "Conversation request completed | turn=%s | prompt_tokens=%s | output_tokens=%s | total_tokens=%s",
            index,
            prompt_tokens,
            output_tokens,
            request_total,
        )

    print("\n=== Conversation Summary ===")
    print(f"Prompt tokens:  {total_prompt_tokens}")
    print(f"Output tokens:  {total_output_tokens}")
    print(f"Total tokens:   {total_tokens}")


print("=== Token Usage Tracking ===")
print(f"Model: {model}")

run_request(
    "Explain artificial intelligence in one sentence."
)

run_conversation()
