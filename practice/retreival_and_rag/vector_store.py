import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"

OUTPUT_PATH = Path(__file__).resolve().parent / "output"

STORE_PATH = OUTPUT_PATH / "vector_store.json"

env_path = Path(__file__).resolve().parent / ".env"

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


# === Embedding ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=model,
        contents=text,
    )

    return response.embeddings[0].values


# === Document Metadata ===

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


# === Vector Record ===

def create_vector_record(
    file_path: Path,
    chunk: str,
    chunk_number: int,
) -> dict:
    """Creates one vector-store record."""

    metadata = create_metadata(
        file_path,
        chunk_number,
    )

    embedding = generate_embedding(
        chunk
    )

    return {
        "id": (
            f"{file_path.stem}"
            f"_chunk_{chunk_number}"
        ),
        "text": chunk,
        "embedding": embedding,
        "metadata": metadata,
    }


# === Build Vector Store ===

def build_vector_store(
    file_path: Path,
    chunks: list[str],
) -> list[dict]:
    """Builds vector records from prepared chunks."""

    records = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        record = create_vector_record(
            file_path,
            chunk,
            index,
        )

        records.append(record)

    return records


# === Save Vector Store ===

def save_vector_store(
    records: list[dict],
    store_path: Path,
):
    """Saves vector records to a JSON file."""

    store_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    store_path.write_text(
        json.dumps(
            records,
            indent=2,
        ),
        encoding="utf-8",
    )


# === Load Vector Store ===

def load_vector_store(
    store_path: Path,
) -> list[dict]:
    """Loads vector records from a JSON file."""

    return json.loads(
        store_path.read_text(
            encoding="utf-8"
        )
    )


# === Prepared Chunks ===

SOURCE_FILE = PATH / "rag.txt"

CHUNKS = [
    """
    Retrieval-Augmented Generation, commonly called RAG,
    combines information retrieval with language generation.
    """,

    """
    A RAG system first searches a collection of documents
    for information relevant to a user's question.
    The retrieved information is then provided to the
    language model as context.
    """,

    """
    The language model uses the retrieved context to
    generate an answer. This allows an application to use
    information that may not have been part of the model's
    original training data.
    """,
]


# === Build ===

print("=== Building Vector Store ===")

records = build_vector_store(
    SOURCE_FILE,
    CHUNKS,
)

print(
    f"Source: {SOURCE_FILE.name}"
)

print(
    f"Records: {len(records)}"
)


# === Save ===

save_vector_store(
    records,
    STORE_PATH,
)

print(
    f"Saved: {STORE_PATH}"
)


# === Load ===

loaded_records = load_vector_store(
    STORE_PATH
)

print("\n=== Loaded Vector Store ===")

print(
    f"Records: {len(loaded_records)}"
)


# === Inspect Records ===

print("\n=== Vector Records ===")

for record in loaded_records:

    print(
        f"\nID: {record['id']}"
    )

    print(
        f"Source: "
        f"{record['metadata']['source']}"
    )

    print(
        f"Document Type: "
        f"{record['metadata']['document_type']}"
    )

    print(
        f"Chunk: "
        f"{record['metadata']['chunk']}"
    )

    print(
        f"Text: "
        f"{record['text']}"
    )

    print(
        f"Embedding Dimensions: "
        f"{len(record['embedding'])}"
    )
