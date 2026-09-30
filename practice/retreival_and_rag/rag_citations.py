import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

BASE_PATH = Path(__file__).resolve().parent
STORE_PATH = BASE_PATH / "output" / "vector_store.json"

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

model = "gemini-3.5-flash-lite"

QUERY = (
    "How does retrieval augmented generation "
    "use retrieved information?"
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


# === Generate Query Embedding ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model="gemini-embedding-001",
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
        a * b
        for a, b in zip(first, second)
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
    """Retrieves the most relevant documents."""

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

    results = []

    for score, document in scored_documents[:top_k]:

        result = {
            **document,
            "similarity": score,
        }

        results.append(result)

    return results


retrieved_documents = retrieve_documents(
    QUERY,
    records,
    TOP_K,
)


# === Retrieved Documents ===

print("\n=== Query ===")

print(QUERY)

print(
    f"\nTop-K: {TOP_K}"
)

print("\n=== Retrieved Documents ===")

for index, document in enumerate(
    retrieved_documents,
    start=1,
):

    print(
        f"\n[Document {index}]"
    )

    print(
        f"ID: {document['id']}"
    )

    print(
        f"Similarity: "
        f"{document['similarity']:.4f}"
    )

    print(
        f"Source: "
        f"{document['metadata']['source']}"
    )

    print(
        f"Chunk: "
        f"{document['metadata']['chunk']}"
    )


# === Context Assembly ===

def build_context(
    documents: list[dict],
) -> str:
    """Builds model context with source information."""

    context_parts = []

    for document in documents:

        metadata = document["metadata"]

        context_parts.append(
            f"[Source: {metadata['source']} | "
            f"Chunk: {metadata['chunk']}]\n"
            f"{document['text']}"
        )

    return "\n\n".join(
        context_parts
    )


context = build_context(
    retrieved_documents
)


# === Generate Answer ===

def generate_answer(
    query: str,
    context: str,
) -> str:
    """Generates an answer using retrieved context."""

    prompt = f"""
Answer the user's question using only the
provided context.

Include source references in the answer using
the format [Source: filename | Chunk: number].

If the context does not contain enough information
to answer the question, say so.

Context:
{context}

Question:
{query}
"""

    response = client.models.generate_content(
        model=model,
        contents=prompt,
    )

    return response.text


print("\n=== Generating Answer ===")

answer = generate_answer(
    QUERY,
    context,
)


# === Answer ===

print("\n=== RAG Answer ===")

print(answer)


# === Sources ===

print("\n=== Sources ===")

seen_sources = set()

for document in retrieved_documents:

    metadata = document["metadata"]

    source_key = (
        metadata["source"],
        metadata["chunk"],
    )

    if source_key in seen_sources:
        continue

    seen_sources.add(
        source_key
    )

    print(
        f"- {metadata['source']} "
        f"| Chunk: {metadata['chunk']}"
    )
