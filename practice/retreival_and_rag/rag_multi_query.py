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
    "How does RAG use retrieved information "
    "and why does this improve answers?"
)

QUERY_COUNT = 3
TOP_K_PER_QUERY = 2


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


# === Generate Queries ===

def generate_queries(
    query: str,
    query_count: int,
) -> list[str]:
    """Generates multiple retrieval queries."""

    prompt = f"""
Generate {query_count} different search queries
for the following user question.

Each query should preserve the original meaning
while approaching the information from a different
retrieval perspective.

Return only the queries, one per line.
Do not number them.

User question:
{query}
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    queries = [
        line.strip()
        for line in response.text.splitlines()
        if line.strip()
    ]

    return queries[:query_count]


queries = generate_queries(
    QUERY,
    QUERY_COUNT,
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


# === Retrieve For Query ===

def retrieve_for_query(
    query: str,
    documents: list[dict],
    top_k: int,
) -> list[dict]:
    """Retrieves the top-K documents for one query."""

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


# === Multi-Query Retrieval ===

def multi_query_retrieval(
    queries: list[str],
    documents: list[dict],
    top_k: int,
) -> list[dict]:
    """Retrieves documents across multiple queries."""

    results_by_id = {}

    for query in queries:

        results = retrieve_for_query(
            query,
            documents,
            top_k,
        )

        for result in results:

            document_id = result["id"]

            existing = results_by_id.get(
                document_id
            )

            if (
                existing is None
                or result["similarity"]
                > existing["similarity"]
            ):
                results_by_id[document_id] = {
                    **result,
                    "matched_query": query,
                }

    return sorted(
        results_by_id.values(),
        key=lambda item: item["similarity"],
        reverse=True,
    )


retrieved_documents = multi_query_retrieval(
    queries,
    records,
    TOP_K_PER_QUERY,
)


# === Output ===

print("\n=== Original Query ===")

print(QUERY)

print("\n=== Generated Queries ===")

for index, query in enumerate(
    queries,
    start=1,
):

    print(
        f"[Query {index}] {query}"
    )


# === Retrieval Results ===

print("\n=== Multi-Query Retrieval Results ===")

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
        f"Matched Query: "
        f"{document['matched_query']}"
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
