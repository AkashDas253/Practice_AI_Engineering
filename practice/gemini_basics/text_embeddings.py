import os
import time
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

model = "gemini-embedding-001"


# ==== TEXT TO EMBED ====

print("\n==== TEXT TO EMBED ====")

text_to_embed = (
    "Vector embeddings capture semantic relationships "
    "in multi-dimensional space."
)

print(text_to_embed)


# ==== TOKEN COUNT ====

print("\n==== TOKEN COUNT ====")

try:
    token_count = client.models.count_tokens(
        model=model,
        contents=text_to_embed,
    )

    print(f"Input tokens: {token_count.total_tokens}")

except Exception as e:
    print("\n==== TOKEN COUNT ERROR ====")
    print(type(e).__name__)
    print(e)


# ==== GENERATE TEXT EMBEDDING ====

print("\n==== GENERATING TEXT EMBEDDING ====")

try:
    start_time = time.perf_counter()

    response = client.models.embed_content(
        model=model,
        contents=text_to_embed,
        config=types.EmbedContentConfig(
            task_type="SEMANTIC_SIMILARITY",
            output_dimensionality=768,
        ),
    )

    elapsed = time.perf_counter() - start_time

    print("Embedding generated successfully!")
    print(f"Model: {model}")
    print("Task Type: SEMANTIC_SIMILARITY")
    print(f"Response time: {elapsed:.3f} seconds")

except Exception as e:
    print("\n==== EMBEDDING ERROR ====")
    print(type(e).__name__)
    print(e)
    raise


# ==== EMBEDDING DETAILS ====

print("\n==== EMBEDDING DETAILS ====")

embedding_vector = response.embeddings[0].values

print(f"Vector Dimensions: {len(embedding_vector)}")
print(f"First 5 Values: {embedding_vector[:5]}...")


# ==== COMPLETE ====

print("\n==== DEMO COMPLETE ====")

time.sleep(2)
