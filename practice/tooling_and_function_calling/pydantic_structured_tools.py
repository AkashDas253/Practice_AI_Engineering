import os
import time
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel, Field
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

class FilterCriteria(BaseModel):
    min_price: float = Field(description="Minimum item price filter in USD")
    max_price: float = Field(description="Maximum item price filter in USD")
    category: str = Field(description="Product category filter (e.g. 'electronics', 'books')")

def search_catalog_with_filters(criteria: FilterCriteria) -> str:
    """Searches product catalog using structured multi-field filter criteria."""

    print("\n[Tool Call] search_catalog_with_filters")
    print(f"[Tool Arguments] {criteria.model_dump()}")

    result = (
        f"Catalog Filter Applied -> Category: '{criteria.category}', "
        f"Price Range: ${criteria.min_price} - ${criteria.max_price}. Found 4 matching items."
    )

    print(f"[Tool Result] {result}")

    return result

config = types.GenerateContentConfig(tools=[search_catalog_with_filters])

print("Creating chat session with Pydantic structured tool parameters...")
chat = client.chats.create(model=model, config=config)

print("Sending request with multi-parameter filter requirements...")
response = chat.send_message("Find me electronics items that cost between $50 and $200.")

print("\n=== STRUCTURED TOOL RESPONSE ===")
print(response.text)

time.sleep(.5)
