import os
import json
import math
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

PATH = Path(__file__).resolve().parent

OUTPUT_PATH = PATH / "output"

STORE_PATH = OUTPUT_PATH / "vector_store.json"

env_path = PATH / ".env"

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

TOP_K = 3

SIMILARITY_THRESHOLD = 0.50


# === Load Vector Store ===

def load_vector_store(
    store_path: Path,
) -> list[dict]:
    """Loads vector records from disk."""

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


# === Query Embedding ===

def generate_query_embedding(
    query: str,
) -> list[float]:
    """Generates an embedding for the search query."""

    response = client.models.embed_content(
        model=model,
        contents=query,
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
        / (
            first_magnitude
            * second_magnitude
        )
    )


# === Score Records ===

def score_records(
    query_embedding: list[float],
    records: list[dict],
) -> list[dict]:
    """Calculates similarity between query and stored records."""

    scored_records = []

    for record in records:

        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_records.append(
            {
                **record,
                "similarity": score,
            }
        )

    return scored_records


# === Top-K Selection ===

def select_top_k(
    records: list[dict],
    top_k: int,
) -> list[dict]:
    """Returns the highest-scoring records."""

    sorted_records = sorted(
        records,
        key=lambda record: record["similarity"],
        reverse=True,
    )

    return sorted_records[:top_k]


# === Similarity Threshold ===

def apply_similarity_threshold(
    records: list[dict],
    threshold: float,
) -> list[dict]:
    """Keeps records meeting the minimum similarity."""

    return [
        record
        for record in records
        if record["similarity"] >= threshold
    ]


# === Search ===

def semantic_search(
    query: str,
    records: list[dict],
    top_k: int = 3,
    threshold: float = 0.50,
) -> list[dict]:
    """Performs semantic retrieval with filtering."""

    query_embedding = generate_query_embedding(
        query
    )

    scored_records = score_records(
        query_embedding,
        records,
    )

    filtered_records = apply_similarity_threshold(
        scored_records,
        threshold,
    )

    return select_top_k(
        filtered_records,
        top_k,
    )


# === Query ===

query = (
    "How does retrieval augmented generation "
    "use retrieved information?"
)

print("\n=== Query ===")

print(query)

print(
    f"\nTop-K: {TOP_K}"
)

print(
    f"Similarity Threshold: "
    f"{SIMILARITY_THRESHOLD:.2f}"
)


# === Search ===

results = semantic_search(
    query,
    records,
    top_k=TOP_K,
    threshold=SIMILARITY_THRESHOLD,
)


# === Results ===

print("\n=== Semantic Search Results ===")

if not results:

    print(
        "No documents met the similarity threshold."
    )

else:

    for index, result in enumerate(
        results,
        start=1,
    ):

        print(
            f"\n[Result {index}]"
        )

        print(
            f"ID: {result['id']}"
        )

        print(
            f"Similarity: "
            f"{result['similarity']:.4f}"
        )

        print(
            f"Source: "
            f"{result['metadata']['source']}"
        )

        print(
            f"Chunk: "
            f"{result['metadata']['chunk']}"
        )

        print(
            f"Text: "
            f"{result['text']}"
        )
