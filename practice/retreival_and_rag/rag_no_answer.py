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
    "What are the safety requirements "
    "for operating a nuclear reactor?"
)

TOP_K = 3
SIMILARITY_THRESHOLD = 0.80


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


# === Retrieval ===

def retrieve_documents(
    query: str,
    documents: list[dict],
    top_k: int,
) -> list[dict]:
    """Retrieves the highest-scoring documents."""

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

        results.append(
            {
                **document,
                "similarity": score,
            }
        )

    return results


# === Query ===

print("\n=== Query ===")

print(QUERY)

print(
    f"\nTop-K: {TOP_K}"
)

print(
    f"Similarity Threshold: "
    f"{SIMILARITY_THRESHOLD:.2f}"
)


# === Retrieve ===

retrieved_documents = retrieve_documents(
    QUERY,
    records,
    TOP_K,
)


# === Retrieval Results ===

print("\n=== Retrieval Results ===")

for index, document in enumerate(
    retrieved_documents,
    start=1,
):

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
        f"Source: "
        f"{document['metadata']['source']}"
    )

    print(
        f"Chunk: "
        f"{document['metadata']['chunk']}"
    )


# === Relevance Check ===

def filter_relevant_documents(
    documents: list[dict],
    threshold: float,
) -> list[dict]:
    """Keeps documents meeting the similarity threshold."""

    return [
        document
        for document in documents
        if document["similarity"] >= threshold
    ]


relevant_documents = filter_relevant_documents(
    retrieved_documents,
    SIMILARITY_THRESHOLD,
)


# === No-Answer Decision ===

print("\n=== Relevance Check ===")

print(
    f"Relevant documents: "
    f"{len(relevant_documents)}"
)

if not relevant_documents:

    print(
        "\n[No Answer]"
    )

    print(
        "No sufficiently relevant information "
        "was found in the retrieved documents."
    )

else:

    # === Context ===

    def build_context(
        documents: list[dict],
    ) -> str:
        """Builds context from relevant documents."""

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
        relevant_documents
    )


    # === Generate Answer ===

    def generate_answer(
        query: str,
        context: str,
    ) -> str:
        """Generates an answer from relevant context."""

        prompt = f"""
Answer the question using only the provided context.

If the context does not contain enough information
to answer the question, say that the information
is not available in the provided documents.

Context:
{context}

Question:
{query}
"""

        response = client.models.generate_content(
            model=GENERATION_MODEL,
            contents=prompt,
        )

        return response.text


    print("\n=== Generating Answer ===")

    answer = generate_answer(
        QUERY,
        context,
    )

    print("\n=== RAG Answer ===")

    print(answer)
