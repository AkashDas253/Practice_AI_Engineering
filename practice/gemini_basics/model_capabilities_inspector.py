import os
from pathlib import Path
from dotenv import load_dotenv
from google import genai

# Load API key
env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env")

client = genai.Client(api_key=api_key)


# ============================================================
# List Models
# ============================================================

models = list(client.models.list())

print(f"\nTotal models available: {len(models)}")


# ============================================================
# Model Details Table
# ============================================================

print("\n=== AVAILABLE MODELS ===\n")

headers = [
    "Model",
    "Display Name",
    "Input Limit",
    "Output Limit",
    "Input Modalities",
    "Output Modalities",
    "Actions",
]

rows = []

for model in models:
    rows.append([
        model.name,
        getattr(model, "display_name", "-"),
        getattr(model, "input_token_limit", "-"),
        getattr(model, "output_token_limit", "-"),
        ", ".join(getattr(model, "input_modalities", []) or []) or "-",
        ", ".join(getattr(model, "output_modalities", []) or []) or "-",
        ", ".join(getattr(model, "supported_actions", []) or []) or "-",
    ])


# Simple table printer
widths = [
    max(len(str(row[i])) for row in [headers] + rows)
    for i in range(len(headers))
]

separator = "+".join("-" * (width + 2) for width in widths)

print(separator)
print("| " + " | ".join(
    str(headers[i]).ljust(widths[i])
    for i in range(len(headers))
) + " |")
print(separator)

for row in rows:
    print("| " + " | ".join(
        str(row[i]).ljust(widths[i])
        for i in range(len(headers))
    ) + " |")

print(separator)


# ============================================================
# Models Supporting generateContent
# ============================================================

print("\n=== MODELS SUPPORTING generateContent ===")

generate_models = []

for model in models:
    actions = getattr(model, "supported_actions", []) or []

    if "generateContent" in actions:
        generate_models.append(model)

for model in generate_models:
    print(f"- {model.name}")

print(f"\nTotal generateContent models: {len(generate_models)}")
