import os
import time
from pathlib import Path
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load .env sitting in the same folder as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise RuntimeError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"


# Simple in-memory storage
memory = {}


# Tool: Save information to memory
def save_memory(key: str, value: str) -> str:
    """Stores information in agent memory."""

    print("\n[Memory Write]")
    print(f"[Key] {key}")
    print(f"[Value] {value}")

    memory[key] = value

    result = f"Memory saved: {key} = {value}"

    print(f"[Memory Result] {result}")

    return result


# Tool: Read information from memory
def read_memory(key: str) -> str:
    """Retrieves information from agent memory."""

    print("\n[Memory Read]")
    print(f"[Key] {key}")

    if key in memory:
        result = f"Memory found: {key} = {memory[key]}"
    else:
        result = f"No memory found for key: {key}"

    print(f"[Memory Result] {result}")

    return result


# Configure the agent
config = types.GenerateContentConfig(
    system_instruction=(
        "You are an assistant with simple persistent memory. "
        "Save useful user information when asked. "
        "Reuse information from memory when it is relevant."
    ),
    tools=[
        save_memory,
        read_memory,
    ],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

print("Creating agent with memory...")
chat = client.chats.create(
    model=model,
    config=config,
)


def run_agent_turn(user_input: str):
    """Runs one agent turn and handles memory tools."""

    print("\n================================")
    print("[USER]")
    print(user_input)

    response = chat.send_message(user_input)

    while response.function_calls:

        for call in response.function_calls:

            print(f"\n[Agent Action] {call.name}")
            print(f"[Arguments] {call.args}")

            if call.name == "save_memory":

                result = save_memory(**call.args)

            elif call.name == "read_memory":

                result = read_memory(**call.args)

            else:

                result = "Unknown tool requested."

            # Send the memory operation result back to the agent
            response = chat.send_message(
                types.Part.from_function_response(
                    name=call.name,
                    response={"result": result},
                )
            )

    print("\n[Agent Response]")
    print(response.text)


# Turn 1: Store information
run_agent_turn(
    "Remember that my favorite programming language is Python."
)

time.sleep(0.5)


# Turn 2: Store another piece of information
run_agent_turn(
    "Also remember that I prefer simple explanations."
)

time.sleep(0.5)


# Turn 3: Reuse stored information
run_agent_turn(
    "What programming language do I prefer, and how should you explain things to me?"
)

time.sleep(0.5)


print("\n================================")
print("=== CURRENT MEMORY ===")
print(memory)
