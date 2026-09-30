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

CANDIDATE_K = 3

TOP_K = 2


# === Environment ===

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
    """Generates an embedding for the query."""

    response = client.models.embed_content(
        model=model,
        contents=query,
    )

    return response.embeddings[0].values


# === Cosine Similarity ===

def cosine_similarity(
    vector_a: list[float],
    vector_b: list[float],
) -> float:
    """Calculates cosine similarity between two vectors."""

    dot_product = sum(
        a * b
        for a, b in zip(
            vector_a,
            vector_b,
        )
    )

    magnitude_a = math.sqrt(
        sum(
            value * value
            for value in vector_a
        )
    )

    magnitude_b = math.sqrt(
        sum(
            value * value
            for value in vector_b
        )
    )

    if magnitude_a == 0 or magnitude_b == 0:
        return 0.0

    return dot_product / (
        magnitude_a * magnitude_b
    )


# === Candidate Retrieval ===

def retrieve_candidates(
    query_embedding: list[float],
    records: list[dict],
    candidate_k: int,
) -> list[dict]:
    """Retrieves an initial candidate set using vector similarity."""

    candidates = []

    for record in records:

        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        candidates.append(
            {
                **record,
                "retrieval_score": score,
            }
        )

    candidates.sort(
        key=lambda record: record["retrieval_score"],
        reverse=True,
    )

    return candidates[:candidate_k]


# === Reranking Score ===

def calculate_rerank_score(
    query: str,
    text: str,
) -> int:
    """Calculates a simple lexical relevance score."""

    query_words = set(
        query.lower().split()
    )

    text_words = set(
        text.lower().split()
    )

    return len(
        query_words.intersection(
            text_words
        )
    )


# === Reranking ===

def rerank_candidates(
    query: str,
    candidates: list[dict],
) -> list[dict]:
    """Reranks retrieved candidates using a second relevance signal."""

    reranked = []

    for candidate in candidates:

        rerank_score = calculate_rerank_score(
            query,
            candidate["text"],
        )

        reranked.append(
            {
                **candidate,
                "rerank_score": rerank_score,
            }
        )

    reranked.sort(
        key=lambda record: (
            record["rerank_score"],
            record["retrieval_score"],
        ),
        reverse=True,
    )

    return reranked


# === Query ===

query = (
    "How does retrieval augmented generation "
    "use retrieved information?"
)

print("\n=== Query ===")

print(query)

print(
    f"\nCandidate K: {CANDIDATE_K}"
)

print(
    f"Final K: {TOP_K}"
)


# === Generate Query Embedding ===

query_embedding = generate_query_embedding(
    query
)


# === Initial Retrieval ===

candidates = retrieve_candidates(
    query_embedding,
    records,
    CANDIDATE_K,
)

print("\n=== Initial Candidates ===")

for index, candidate in enumerate(
    candidates,
    start=1,
):

    print(
        f"\n[Candidate {index}]"
    )

    print(
        f"ID: {candidate['id']}"
    )

    print(
        f"Retrieval Score: "
        f"{candidate['retrieval_score']:.4f}"
    )


# === Rerank ===

reranked_records = rerank_candidates(
    query,
    candidates,
)


# === Final Results ===

final_results = reranked_records[:TOP_K]

print("\n=== Reranked Results ===")

for index, result in enumerate(
    final_results,
    start=1,
):

    print(
        f"\n[Result {index}]"
    )

    print(
        f"ID: {result['id']}"
    )

    print(
        f"Retrieval Score: "
        f"{result['retrieval_score']:.4f}"
    )

    print(
        f"Rerank Score: "
        f"{result['rerank_score']}"
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


# === Strategy ===

print("\n=== Retrieval Strategy ===")

print(
    "Stage 1: Retrieve an initial candidate set."
)

print(
    "Stage 2: Apply a second relevance score."
)

print(
    "Stage 3: Keep the highest-ranked candidates."
)
