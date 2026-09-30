import os
import json
import math
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# === Config ===

PATH = Path(__file__).resolve().parent

STORE_PATH = PATH / "output" / "vector_store.json"

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

generation_model = "models/gemini-3.5-flash-lite"

embedding_model = "gemini-embedding-001"

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


# === Generate Query Embedding ===

def generate_query_embedding(
    query: str,
) -> list[float]:
    """Generates an embedding for the query."""

    response = client.models.embed_content(
        model=embedding_model,
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


# === Retrieve Grounding Context ===

def retrieve_chunks(
    query: str,
    records: list[dict],
    top_k: int,
    threshold: float,
) -> list[dict]:
    """Retrieves chunks that meet the similarity threshold."""

    query_embedding = generate_query_embedding(
        query
    )

    scored_records = []

    for record in records:

        score = cosine_similarity(
            query_embedding,
            record["embedding"],
        )

        if score >= threshold:

            scored_records.append(
                {
                    "record": record,
                    "score": score,
                }
            )

    scored_records.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return scored_records[:top_k]


# === Assemble Grounding Context ===

def assemble_context(
    results: list[dict],
) -> str:
    """Builds context from retrieved records."""

    sections = []

    for result in results:

        record = result["record"]

        source = record["metadata"]["source"]

        chunk = record["metadata"]["chunk"]

        text = record["text"].strip()

        sections.append(
            f"[Source: {source} | Chunk: {chunk}]\n"
            f"{text}"
        )

    return "\n\n".join(
        sections
    )


# === Generate Grounded Answer ===

def generate_grounded_answer(
    query: str,
    context: str,
) -> str:
    """Generates an answer using only the retrieved context."""

    prompt = f"""
You are answering a question using retrieved documents.

Grounding rules:
- Use only information supported by the provided context.
- Do not add facts from your general knowledge.
- Do not invent information.
- If the context does not contain enough information, say:
  "The provided context does not contain enough information to answer this question."
- Keep the answer concise and directly answer the question.

Retrieved Context:
{context}

Question:
{query}

Answer:
"""

    response = client.models.generate_content(
        model=generation_model,
        contents=prompt,
        config=types.GenerateContentConfig(
            temperature=0.2,
            automatic_function_calling=types.AutomaticFunctionCallingConfig(
                disable=True
            ),
        ),
    )

    return response.text


# === User Query ===

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


# === Retrieval ===

results = retrieve_chunks(
    query,
    records,
    TOP_K,
    SIMILARITY_THRESHOLD,
)

print("\n=== Grounding Documents ===")

if not results:

    print(
        "No sufficiently relevant documents found."
    )

else:

    for index, result in enumerate(
        results,
        start=1,
    ):

        record = result["record"]

        print(
            f"\n[Document {index}]"
        )

        print(
            f"ID: {record['id']}"
        )

        print(
            f"Similarity: "
            f"{result['score']:.4f}"
        )

        print(
            f"Source: "
            f"{record['metadata']['source']}"
        )

        print(
            f"Chunk: "
            f"{record['metadata']['chunk']}"
        )


# === Context ===

if results:

    context = assemble_context(
        results
    )

    print("\n=== Grounding Context ===")

    print(context)

else:

    context = ""


# === Generation ===

print("\n=== Generating Grounded Answer ===")

if not context:

    print(
        "\n=== RAG Answer ==="
    )

    print(
        "The provided context does not contain "
        "enough information to answer this question."
    )

else:

    answer = generate_grounded_answer(
        query,
        context,
    )

    print("\n=== RAG Answer ===")

    print(answer)
