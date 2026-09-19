import os
import json
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types


# ==== SETUP ====

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# ==== CODE EXECUTION ====

print("\n==== CODE EXECUTION ====")

config = types.GenerateContentConfig(
    tools=[
        types.Tool(
            code_execution=types.ToolCodeExecution
        )
    ]
)

chat = client.chats.create(
    model=model,
    config=config,
)

prompt = (
    "Calculate the 50th Fibonacci number using Python. "
    "Generate and run the Python code."
)

response = chat.send_message(prompt)

print(response.text)


# ==== EXECUTABLE CODE ====

print("\n==== EXECUTABLE CODE ====")

if response.candidates:
    for part in response.candidates[0].content.parts:
        if part.executable_code:
            print(f"Language: {part.executable_code.language}")
            print(part.executable_code.code)


# ==== EXECUTION RESULT ====

print("\n==== EXECUTION RESULT ====")

if response.candidates:
    for part in response.candidates[0].content.parts:
        if part.code_execution_result:
            print(f"Outcome: {part.code_execution_result.outcome}")
            print(f"Output: {part.code_execution_result.output}")


# ==== ANOTHER CALCULATION ====

print("\n==== ANOTHER CALCULATION ====")

response = chat.send_message(
    "Using Python, calculate the sum of the first 100 prime numbers."
)

print(response.text)


# ==== CHAT HISTORY ====

print("\n==== CHAT HISTORY ====")

for message in chat.get_history():
    print(f"\nRole: {message.role}")

    for part in message.parts:
        if part.text:
            print(f"Text: {part.text}")

        if part.executable_code:
            print("\nPython code:")
            print(part.executable_code.code)

        if part.code_execution_result:
            print("\nExecution result:")
            print(part.code_execution_result.output)


# ==== TOKEN USAGE ====

print("\n==== TOKEN USAGE ====")

if response.usage_metadata:
    usage = response.usage_metadata

    print(f"Input tokens:  {usage.prompt_token_count}")
    print(f"Output tokens: {usage.candidates_token_count}")
    print(f"Total tokens:  {usage.total_token_count}")


# ==== RAW RESPONSE ====

print("\n==== RAW RESPONSE ====")

print(json.dumps(
    response.model_dump(exclude_none=True),
    indent=2,
    default=str,
))
