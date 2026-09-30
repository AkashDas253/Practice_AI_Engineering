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
    "How does retrieval augmented generation "
    "use retrieved information?"
)

TOP_K = 3
SIMILARITY_THRESHOLD = 0.50


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
    threshold: float,
) -> list[dict]:
    """Retrieves relevant documents."""

    query_embedding = generate_embedding(
        query
    )

    scored_documents = []

    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        if score >= threshold:

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


retrieved_documents = retrieve_documents(
    QUERY,
    records,
    TOP_K,
    SIMILARITY_THRESHOLD,
)


# === Build Context ===

def build_context(
    documents: list[dict],
) -> str:
    """Builds context from retrieved documents."""

    sections = []

    for document in documents:

        metadata = document["metadata"]

        sections.append(
            (
                f"[Source: {metadata['source']} | "
                f"Chunk: {metadata['chunk']}]\n"
                f"{document['text']}"
            )
        )

    return "\n\n".join(
        sections
    )


context = build_context(
    retrieved_documents
)


# === Generate Answer ===

def generate_answer(
    query: str,
    context: str,
) -> str:
    """Generates an answer from retrieved context."""

    prompt = f"""
Answer the question using only the provided
retrieved context.

Do not introduce unsupported information.

Question:
{query}

Retrieved context:
{context}

Answer:
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text.strip()


answer = generate_answer(
    QUERY,
    context,
)


# === Retrieval Evaluation ===

def evaluate_retrieval(
    documents: list[dict],
) -> dict:
    """Evaluates basic retrieval quality signals."""

    similarities = [
        document["similarity"]
        for document in documents
    ]

    return {
        "retrieved_count": len(documents),
        "top_similarity": (
            max(similarities)
            if similarities
            else 0.0
        ),
        "average_similarity": (
            sum(similarities)
            / len(similarities)
            if similarities
            else 0.0
        ),
    }


retrieval_metrics = evaluate_retrieval(
    retrieved_documents
)


# === Answer Evaluation ===

def evaluate_answer(
    query: str,
    context: str,
    answer: str,
) -> dict:
    """Evaluates answer quality using defined RAG criteria."""

    prompt = f"""
Evaluate the following RAG answer.

Question:
{query}

Retrieved context:
{context}

Answer:
{answer}

Evaluate these criteria:

1. Groundedness:
Is the answer supported by the retrieved context?

2. Relevance:
Does the answer directly address the question?

3. Completeness:
Does the answer include the important information
available in the retrieved context?

Return only valid JSON using this structure:

{{
  "groundedness": 0,
  "relevance": 0,
  "completeness": 0,
  "explanation": "short explanation"
}}

Use scores from 0 to 1.
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    text = response.text.strip()

    if text.startswith("```"):
        text = text.replace(
            "```json",
            "",
        ).replace(
            "```",
            "",
        ).strip()

    return json.loads(
        text
    )


answer_metrics = evaluate_answer(
    QUERY,
    context,
    answer,
)


# === Output ===

print("\n=== Evaluation Query ===")

print(QUERY)

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


# === Retrieval Metrics ===

print("\n=== Retrieval Evaluation ===")

print(
    f"Retrieved Documents: "
    f"{retrieval_metrics['retrieved_count']}"
)

print(
    f"Top Similarity: "
    f"{retrieval_metrics['top_similarity']:.4f}"
)

print(
    f"Average Similarity: "
    f"{retrieval_metrics['average_similarity']:.4f}"
)


# === Generated Answer ===

print("\n=== RAG Answer ===")

print(answer)


# === Answer Metrics ===

print("\n=== Answer Evaluation ===")

print(
    f"Groundedness: "
    f"{answer_metrics['groundedness']}"
)

print(
    f"Relevance: "
    f"{answer_metrics['relevance']}"
)

print(
    f"Completeness: "
    f"{answer_metrics['completeness']}"
)

print(
    f"Explanation: "
    f"{answer_metrics['explanation']}"
)
