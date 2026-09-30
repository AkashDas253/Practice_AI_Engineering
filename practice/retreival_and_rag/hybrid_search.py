import json
import math
import re
from pathlib import Path

from google import genai
from dotenv import load_dotenv
import os


# === Config ===

PATH = Path(__file__).resolve().parent

OUTPUT_PATH = PATH / "output"

STORE_PATH = OUTPUT_PATH / "vector_store.json"

env_path = PATH / ".env"

TOP_K = 3

KEYWORD_WEIGHT = 0.3

SEMANTIC_WEIGHT = 0.7


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


# === Tokenize ===

def tokenize(
    text: str,
) -> list[str]:
    """Converts text into normalized word tokens."""

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )


# === Keyword Score ===

def keyword_score(
    query: str,
    text: str,
) -> int:
    """Counts unique query words found in the document."""

    query_words = set(
        tokenize(query)
    )

    text_words = set(
        tokenize(text)
    )

    return len(
        query_words.intersection(
            text_words
        )
    )


# === Query Embedding ===

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


# === Normalize Scores ===

def normalize_scores(
    records: list[dict],
    field: str,
) -> list[dict]:
    """Normalizes scores to a 0-1 range."""

    scores = [
        record[field]
        for record in records
    ]

    maximum = max(
        scores,
        default=0,
    )

    minimum = min(
        scores,
        default=0,
    )

    if maximum == minimum:

        for record in records:
            record[f"{field}_normalized"] = (
                1.0 if maximum > 0 else 0.0
            )

        return records

    for record in records:

        record[f"{field}_normalized"] = (
            record[field] - minimum
        ) / (
            maximum - minimum
        )

    return records


# === Hybrid Score ===

def calculate_hybrid_score(
    record: dict,
) -> float:
    """Combines keyword and semantic scores."""

    keyword_component = (
        record["keyword_score_normalized"]
        * KEYWORD_WEIGHT
    )

    semantic_component = (
        record["semantic_score_normalized"]
        * SEMANTIC_WEIGHT
    )

    return (
        keyword_component
        + semantic_component
    )


# === Hybrid Search ===

def hybrid_search(
    query: str,
    records: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Combines lexical and semantic retrieval."""

    query_embedding = generate_embedding(
        query
    )

    scored_records = []

    for record in records:

        keyword_score_value = keyword_score(
            query,
            record["text"],
        )

        semantic_score_value = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        scored_records.append(
            {
                **record,
                "keyword_score": keyword_score_value,
                "semantic_score": semantic_score_value,
            }
        )

    normalize_scores(
        scored_records,
        "keyword_score",
    )

    normalize_scores(
        scored_records,
        "semantic_score",
    )

    for record in scored_records:

        record["hybrid_score"] = (
            calculate_hybrid_score(
                record
            )
        )

    return sorted(
        scored_records,
        key=lambda record: record["hybrid_score"],
        reverse=True,
    )[:top_k]


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
    f"Keyword Weight: {KEYWORD_WEIGHT}"
)

print(
    f"Semantic Weight: {SEMANTIC_WEIGHT}"
)


# === Search ===

results = hybrid_search(
    query,
    records,
    top_k=TOP_K,
)


# === Results ===

print("\n=== Hybrid Search Results ===")

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
        f"Keyword Score: "
        f"{result['keyword_score']}"
    )

    print(
        f"Semantic Score: "
        f"{result['semantic_score']:.4f}"
    )

    print(
        f"Hybrid Score: "
        f"{result['hybrid_score']:.4f}"
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


# === Explanation ===

print("\n=== Retrieval Strategy ===")

print(
    "Keyword retrieval provides lexical matching."
)

print(
    "Semantic retrieval provides meaning-based matching."
)

print(
    "Hybrid retrieval combines both signals "
    "into a single ranking score."
)
