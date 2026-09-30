import os
import json
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

BASE_PATH = Path(__file__).resolve().parent

DOCUMENT_PATH = (
    BASE_PATH
    / "documents"
    / "rag.txt"
)

OUTPUT_PATH = (
    BASE_PATH
    / "output"
    / "rag_pipeline.json"
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

CHUNK_SIZE = 300
TOP_K = 3
SIMILARITY_THRESHOLD = 0.50

QUERY = (
    "How does retrieval augmented generation "
    "use retrieved information?"
)


# === Document Ingestion ===

def load_document(
    file_path: Path,
) -> str:
    """Loads a document from a local file."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


document_text = load_document(
    DOCUMENT_PATH
)


# === Text Parsing ===

def normalize_text(
    text: str,
) -> str:
    """Normalizes whitespace in document text."""

    text = text.replace(
        "\r\n",
        "\n",
    )

    text = re.sub(
        r"[ \t]+",
        " ",
        text,
    )

    text = re.sub(
        r"\n{3,}",
        "\n\n",
        text,
    )

    return text.strip()


parsed_text = normalize_text(
    document_text
)


# === Text Chunking ===

def create_chunks(
    text: str,
    chunk_size: int = 300,
) -> list[str]:
    """Splits normalized text into fixed-size chunks."""

    chunks = []

    for index in range(
        0,
        len(text),
        chunk_size,
    ):

        chunk = text[
            index:index + chunk_size
        ].strip()

        if chunk:
            chunks.append(chunk)

    return chunks


chunks = create_chunks(
    parsed_text,
    CHUNK_SIZE,
)


# === Metadata ===

def create_metadata(
    file_path: Path,
    chunk_number: int,
) -> dict:
    """Creates metadata for a document chunk."""

    return {
        "source": file_path.name,
        "title": file_path.stem,
        "document_type": file_path.suffix.lower(),
        "chunk": chunk_number,
    }


# === Embedding Generation ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


# === Vector Records ===

def create_vector_records(
    file_path: Path,
    document_chunks: list[str],
) -> list[dict]:
    """Creates vector records from document chunks."""

    records = []

    for index, chunk in enumerate(
        document_chunks,
        start=1,
    ):

        records.append(
            {
                "id": (
                    f"{file_path.stem}"
                    f"_chunk_{index}"
                ),
                "text": chunk,
                "embedding": generate_embedding(
                    chunk
                ),
                "metadata": create_metadata(
                    file_path,
                    index,
                ),
            }
        )

    return records


vector_records = create_vector_records(
    DOCUMENT_PATH,
    chunks,
)


# === Query Embedding ===

query_embedding = generate_embedding(
    QUERY
)


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
    query_vector: list[float],
    records: list[dict],
    top_k: int,
    threshold: float,
) -> list[dict]:
    """Retrieves relevant chunks using vector similarity."""

    scored_records = []

    for record in records:

        score = cosine_similarity(
            query_vector,
            record["embedding"],
        )

        if score >= threshold:

            scored_records.append(
                (
                    score,
                    record,
                )
            )

    scored_records.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        {
            **record,
            "similarity": score,
        }
        for score, record
        in scored_records[:top_k]
    ]


retrieved_records = retrieve_documents(
    query_embedding,
    vector_records,
    TOP_K,
    SIMILARITY_THRESHOLD,
)


# === Context Construction ===

def build_context(
    records: list[dict],
) -> str:
    """Builds model context from retrieved chunks."""

    sections = []

    for record in records:

        metadata = record["metadata"]

        sections.append(
            (
                f"[Source: {metadata['source']} | "
                f"Chunk: {metadata['chunk']}]\n"
                f"{record['text']}"
            )
        )

    return "\n\n".join(
        sections
    )


context = build_context(
    retrieved_records
)


# === Answer Generation ===

def generate_answer(
    query: str,
    context: str,
) -> str:
    """Generates an answer grounded in retrieved context."""

    prompt = f"""
Answer the question using only the provided
retrieved context.

If the context does not contain enough information,
say that the information is not available.

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


# === Save Pipeline Output ===

def save_pipeline_output(
    output_path: Path,
    records: list[dict],
    retrieved: list[dict],
    answer: str,
) -> None:
    """Saves pipeline results for later inspection."""

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    output = {
        "query": QUERY,
        "source": DOCUMENT_PATH.name,
        "chunks_created": len(chunks),
        "records_created": len(records),
        "retrieved_records": [
            {
                "id": record["id"],
                "similarity": record["similarity"],
                "metadata": record["metadata"],
                "text": record["text"],
            }
            for record in retrieved
        ],
        "context": context,
        "answer": answer,
    }

    output_path.write_text(
        json.dumps(
            output,
            indent=2,
        ),
        encoding="utf-8",
    )


save_pipeline_output(
    OUTPUT_PATH,
    vector_records,
    retrieved_records,
    answer,
)


# === Output ===

print("=== RAG Pipeline ===")

print(
    f"Source: {DOCUMENT_PATH.name}"
)

print(
    f"Chunks created: {len(chunks)}"
)

print(
    f"Vector records: {len(vector_records)}"
)

print(
    f"Query: {QUERY}"
)

print(
    f"Retrieved records: "
    f"{len(retrieved_records)}"
)

print(
    f"Similarity threshold: "
    f"{SIMILARITY_THRESHOLD:.2f}"
)


# === Retrieved Documents ===

print("\n=== Retrieved Documents ===")

for index, record in enumerate(
    retrieved_records,
    start=1,
):

    metadata = record["metadata"]

    print(
        f"\n[Result {index}]"
    )

    print(
        f"ID: {record['id']}"
    )

    print(
        f"Similarity: "
        f"{record['similarity']:.4f}"
    )

    print(
        f"Source: {metadata['source']}"
    )

    print(
        f"Chunk: {metadata['chunk']}"
    )


# === Context ===

print("\n=== Context ===")

print(context)


# === Answer ===

print("\n=== RAG Answer ===")

print(answer)


# === Saved Output ===

print("\n=== Saved Output ===")

print(
    f"Saved: {OUTPUT_PATH}"
)
