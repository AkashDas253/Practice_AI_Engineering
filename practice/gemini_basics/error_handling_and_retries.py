import os
import time
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ClientError


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# ==== GENERATION CONFIG ====

print("\n==== GENERATION CONFIG ====")

config = types.GenerateContentConfig(
    max_output_tokens=100,
)

print(f"Model: {model}")
print("Max output tokens: 100")


# ==== RETRY CONFIGURATION ====

print("\n==== RETRY CONFIGURATION ====")

max_retries = 3
base_wait_time = 5

print(f"Maximum retries: {max_retries}")
print(f"Base wait time: {base_wait_time} seconds")


# ==== GENERATE RESPONSE ====

print("\n==== GENERATING RESPONSE ====")

prompt = "Give me one sentence about Python."

print(f"Prompt: {prompt}")

success = False

for attempt in range(1, max_retries + 1):

    print(f"\nAttempt {attempt}/{max_retries}")

    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
            config=config,
        )

        success = True
        break

    except ClientError as error:

        # ==== RATE LIMIT / QUOTA ERROR ====

        if error.code == 429:

            error_message = str(error)

            print("\n==== 429 RESOURCE EXHAUSTED ====")
            print(error_message)

            # A 429 can mean temporary rate limiting OR
            # a quota that is already exhausted.

            if "quota" in error_message.lower():
                print("\nQuota appears to be exhausted.")
                print("Retrying may not help until the quota resets.")

            if attempt < max_retries:
                wait_time = base_wait_time * attempt

                print(
                    f"Waiting {wait_time} seconds before retry..."
                )

                time.sleep(wait_time)

            else:
                print("\nMaximum retries reached.")

        # ==== MODEL NOT FOUND ====

        elif error.code == 404:

            print("\n==== MODEL NOT FOUND ====")
            print("Model not found or unavailable.")
            print(f"Model: {model}")

            break

        # ==== OTHER API ERROR ====

        else:

            print("\n==== API ERROR ====")
            print(f"Error code: {error.code}")
            print(error)

            break


# ==== RESPONSE ====

if success:

    print("\n==== RESPONSE ====")
    print(response.text)


    # ==== RESPONSE DETAILS ====

    print("\n==== RESPONSE DETAILS ====")

    if response.candidates:
        candidate = response.candidates[0]

        print(f"Finish reason: {candidate.finish_reason}")


    # ==== TOKEN USAGE ====

    print("\n==== TOKEN USAGE ====")

    if response.usage_metadata:
        usage = response.usage_metadata

        print(f"Input tokens:  {usage.prompt_token_count}")
        print(f"Output tokens: {usage.candidates_token_count}")
        print(f"Total tokens:  {usage.total_token_count}")


else:

    print("\n==== GENERATION FAILED ====")
    print("No successful response was generated.")


# ==== COMPLETE ====

print("\n==== DEMO COMPLETE ====")
