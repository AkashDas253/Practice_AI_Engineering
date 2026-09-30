import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

BASE_PATH = Path(__file__).resolve().parent

STORE_PATH = (
    BASE_PATH
    / "output"
    / "vector_store.json"
)

env_path = BASE_PATH / ".env"

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

EMBEDDING_MODEL = "gemini-embedding-001"
GENERATION_MODEL = "gemini-3.5-flash-lite"

QUERY = (
    "How does RAG use the stuff it finds?"
)

TOP_K = 3


# === Load Vector Store ===

def load_vector_store(
    store_path: Path,
) -> list[dict]:
    """Loads vector records from JSON."""

    return json.loads(
        store_path.read_text(
            encoding="utf-8"
        )
    )


records = load_vector_store(
    STORE_PATH
)

print("=== Vector Store ===")

print(
    f"Records loaded: {len(records)}"
)


# === Query Rewriting ===

def rewrite_query(
    query: str,
) -> str:
    """Rewrites a user query for retrieval."""

    prompt = f"""
Rewrite the following user question into a
clear, concise retrieval query.

Preserve the original meaning.
Do not answer the question.
Return only the rewritten query.

User question:
{query}
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text.strip()


rewritten_query = rewrite_query(
    QUERY
)


# === Generate Embedding ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


# === Cosine Similarity ===

def cosine_similarity(
    first: list[float],
    second: list[float],
) -> float:
    """Calculates cosine similarity."""

    dot_product = sum(
        first_value * second_value
        for first_value, second_value
        in zip(first, second)
    )

    first_magnitude = sum(
        value * value
        for value in first
    ) ** 0.5

    second_magnitude = sum(
        value * value
        for value in second
    ) ** 0.5

    if (
        first_magnitude == 0
        or second_magnitude == 0
    ):
        return 0.0

    return (
        dot_product
        / (
            first_magnitude
            * second_magnitude
        )
    )


# === Semantic Retrieval ===

def retrieve_documents(
    query: str,
    documents: list[dict],
    top_k: int,
) -> list[dict]:
    """Retrieves documents using semantic similarity."""

    query_embedding = generate_embedding(
        query
    )

    scored_documents = []

    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        scored_documents.append(
            (
                score,
                document,
            )
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        {
            **document,
            "similarity": score,
        }
        for score, document
        in scored_documents[:top_k]
    ]


# === Retrieval ===

retrieved_documents = retrieve_documents(
    rewritten_query,
    records,
    TOP_K,
)


# === Output ===

print("\n=== Original Query ===")

print(QUERY)

print("\n=== Rewritten Query ===")

print(rewritten_query)

print("\n=== Retrieved Documents ===")

for index, document in enumerate(
    retrieved_documents,
    start=1,
):

    metadata = document["metadata"]

    print(
        f"\n[Result {index}]"
    )

    print(
        f"ID: {document['id']}"
    )

    print(
        f"Similarity: "
        f"{document['similarity']:.4f}"
    )

    print(
        f"Source: {metadata['source']}"
    )

    print(
        f"Chunk: {metadata['chunk']}"
    )

    print(
        f"Text:\n{document['text']}"
    )
