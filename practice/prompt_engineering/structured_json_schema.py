import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

# Load .env file sitting in the same directory as this script
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

# Specify model
model = "models/gemini-3.5-flash-lite"

# Define target Pydantic schema for output validation
class TechnicalSupportSummary(BaseModel):
    user_id: int = Field(description="Unique numeric user ID")
    operating_system: str = Field(description="User operating system name")
    is_resolved: bool = Field(description="True if problem was fixed, False otherwise")
    action_items: list[str] = Field(description="List of concrete steps for Tier 2 support")

# Configure structured JSON output mode
config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=TechnicalSupportSummary,
)

prompt = """
Process this ticket:
User 9482 on macOS Sonoma reports app crash when exporting PDF >50MB. Reinstalling app worked for 1 day. Issue unresolved.
"""

print("Sending structured JSON request with Pydantic schema validation...")
chat = client.chats.create(model=model, config=config)
response = chat.send_message(prompt)

print("\n=== RAW JSON RESPONSE ===")
print(response.text)

# Parse JSON into native Pydantic model
parsed_data = TechnicalSupportSummary.model_validate_json(response.text)
print("\n=== PARSED PYDANTIC OBJECT ===")
print(f"User ID: {parsed_data.user_id}")
print(f"Action Items: {parsed_data.action_items}")

time.sleep(.5)