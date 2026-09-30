import os
import math
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"

env_path = Path(__file__).resolve().parent / ".env"

load_dotenv(
    dotenv_path=env_path
)

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:
    raise RuntimeError(
        "GEMINI_API_KEY not found in .env"
    )

client = genai.Client(
    api_key=api_key
)

model = "gemini-embedding-001"


# === Embedding ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=model,
        contents=text,
    )

    return response.embeddings[0].values


# === Cosine Similarity ===

def cosine_similarity(
    first: list[float],
    second: list[float],
) -> float:
    """Measures similarity between two embeddings."""

    if len(first) != len(second):
        raise ValueError(
            "Embeddings must have the same dimensions."
        )

    dot_product = sum(
        first_value * second_value
        for first_value, second_value
        in zip(first, second)
    )

    first_magnitude = math.sqrt(
        sum(
            value * value
            for value in first
        )
    )

    second_magnitude = math.sqrt(
        sum(
            value * value
            for value in second
        )
    )

    if first_magnitude == 0:
        raise ValueError(
            "First embedding has zero magnitude."
        )

    if second_magnitude == 0:
        raise ValueError(
            "Second embedding has zero magnitude."
        )

    return (
        dot_product
        / (first_magnitude * second_magnitude)
    )


# === Query ===

query = (
    "What is retrieval augmented generation?"
)

print("=== Query ===")
print(query)

query_embedding = generate_embedding(
    query
)


# === Documents ===

documents = [
    (
        "RAG document",
        (
            "Retrieval augmented generation "
            "combines document retrieval with "
            "language model generation."
        ),
    ),
    (
        "Python document",
        (
            "Python is a programming language "
            "used for building many types of "
            "software applications."
        ),
    ),
    (
        "Database document",
        (
            "Databases store and organize "
            "structured information for applications."
        ),
    ),
]


# === Compare Similarity ===

print("\n=== Similarity Scores ===")

results = []

for name, text in documents:

    document_embedding = generate_embedding(
        text
    )

    similarity = cosine_similarity(
        query_embedding,
        document_embedding,
    )

    results.append(
        {
            "name": name,
            "text": text,
            "similarity": similarity,
        }
    )

    print(
        f"\n[Document] {name}"
    )

    print(
        f"[Similarity] "
        f"{similarity:.4f}"
    )


# === Ranked Results ===

results.sort(
    key=lambda item: item["similarity"],
    reverse=True,
)

print("\n=== Ranked Results ===")

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"{index}. "
        f"{result['name']} "
        f"({result['similarity']:.4f})"
    )
