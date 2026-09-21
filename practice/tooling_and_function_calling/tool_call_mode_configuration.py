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

def perform_security_audit(ip_address: str) -> str:
    """Runs a security vulnerability scan on a given IP address."""

    print("\n[Tool Call] perform_security_audit")
    print(f"[Tool Arguments] ip_address={ip_address}")

    result = (
        f"IP {ip_address}: No open critical vulnerabilities detected. "
        f"Port 443 active."
    )

    print(f"[Tool Result] {result}")

    return result

# Force Gemini to execute a tool call regardless of prompt text
config = types.GenerateContentConfig(
    tools=[perform_security_audit],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
    tool_config=types.ToolConfig(
        function_calling_config=types.FunctionCallingConfig(
            mode="ANY",  # Forces tool call
            allowed_function_names=["perform_security_audit"]
        )
    )
)

print("Creating chat session forced into ANY tool-calling mode...")
chat = client.chats.create(model=model, config=config)

print("Sending generic prompt...")
response = chat.send_message(
    "Check the security status for IP address 192.168.1.50"
)

# Inspect requested function calls
if response.function_calls:
    for call in response.function_calls:
        print(f"\n[Intercepted Function Call] Name: {call.name}")
        print(f"[Intercepted Arguments] {call.args}")

        # Manually execute local Python function
        if call.name == "perform_security_audit":
            ip = call.args.get("ip_address", "")
            result = perform_security_audit(ip)

            print("\n=== FORCED TOOL RESPONSE ===")
            print(result)
else:
    print("\nNo function call was requested.")

time.sleep(.5)
