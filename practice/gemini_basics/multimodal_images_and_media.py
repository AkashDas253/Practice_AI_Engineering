import os
import json
from pathlib import Path
from dotenv import load_dotenv
from pydantic import BaseModel
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


# ==== IMAGE ====

print("\n==== IMAGE ====")

dummy_png_bytes = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01\x08\x02"
    b"\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc\xf8\xcf\xc0\x00\x00\x03"
    b"\x01\x01\x00\x18\xdd\x8d\xb0\x00\x00\x00\x00IEND\xaeB`\x82"
)

image_part = types.Part.from_bytes(
    data=dummy_png_bytes,
    mime_type="image/png",
)

response = client.models.generate_content(
    model=model,
    contents=[
        image_part,
        "Describe this image and tell me its dimensions and color.",
    ],
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    ),
)

print(response.text)


# ==== MULTIPLE IMAGES ====

print("\n==== MULTIPLE IMAGES ====")

image_part_2 = types.Part.from_bytes(
    data=dummy_png_bytes,
    mime_type="image/png",
)

response = client.models.generate_content(
    model=model,
    contents=[
        "Compare these two images.",
        image_part,
        image_part_2,
    ],
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    ),
)

print(response.text)


# ==== IMAGE + STRUCTURED OUTPUT ====

print("\n==== IMAGE + STRUCTURED OUTPUT ====")


class ImageInfo(BaseModel):
    width: int
    height: int
    color: str
    description: str


config = types.GenerateContentConfig(
    response_mime_type="application/json",
    response_schema=ImageInfo,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(
        disable=True
    ),
)

response = client.models.generate_content(
    model=model,
    contents=[
        image_part,
        "Analyze this image and return its dimensions, color, and description.",
    ],
    config=config,
)

image_info = ImageInfo.model_validate_json(response.text)

print(f"Width: {image_info.width}")
print(f"Height: {image_info.height}")
print(f"Color: {image_info.color}")
print(f"Description: {image_info.description}")


# ==== MULTIMODAL TOKEN COUNT ====

print("\n==== MULTIMODAL TOKEN COUNT ====")

token_response = client.models.count_tokens(
    model=model,
    contents=[
        image_part,
        "Analyze this image.",
    ],
)

print(f"Input tokens: {token_response.total_tokens}")


# ==== MULTIMODAL STREAMING ====

print("\n==== MULTIMODAL STREAMING ====")

response_stream = client.models.generate_content_stream(
    model=model,
    contents=[
        image_part,
        "Describe this image in detail.",
    ],
    config=types.GenerateContentConfig(
        automatic_function_calling=types.AutomaticFunctionCallingConfig(
            disable=True
        )
    ),
)

for chunk in response_stream:
    if chunk.text:
        print(chunk.text, end="", flush=True)

print()


# ==== MULTIMODAL CHAT ====

print("\n==== MULTIMODAL CHAT ====")

chat = client.chats.create(model=model)

response = chat.send_message([
    image_part,
    "Describe this image.",
])

print(response.text)

response = chat.send_message(
    "What did you say about the image?"
)

print("\nFollow-up:")
print(response.text)


# ==== MULTIMODAL CHAT STREAMING ====

print("\n==== MULTIMODAL CHAT STREAMING ====")

response_stream = chat.send_message_stream([
    image_part,
    "Describe this image in detail.",
])

for chunk in response_stream:
    if chunk.text:
        print(chunk.text, end="", flush=True)

print()


# ==== CHAT HISTORY ====

print("\n==== CHAT HISTORY ====")

for message in chat.get_history():
    print(f"\nRole: {message.role}")

    for part in message.parts:
        if part.text:
            print(f"Text: {part.text}")

        if part.inline_data:
            print(
                f"Media: {part.inline_data.mime_type}, "
                f"{len(part.inline_data.data)} bytes"
            )


# ==== RESPONSE DETAILS ====

print("\n==== RESPONSE DETAILS ====")

if response.candidates:
    candidate = response.candidates[0]

    print(f"Finish reason: {candidate.finish_reason}")
    print(f"Safety ratings: {candidate.safety_ratings}")


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
