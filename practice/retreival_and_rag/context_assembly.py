import json
from pathlib import Path


# === Config ===

PATH = Path(__file__).resolve().parent

STORE_PATH = PATH / "output" / "vector_store.json"

TOP_K = 3


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


# === Select Chunks ===

def select_chunks(
    records: list[dict],
    top_k: int,
) -> list[dict]:
    """Selects the top-K retrieved records."""

    return records[:top_k]


# === Order Chunks ===

def order_chunks(
    records: list[dict],
) -> list[dict]:
    """Orders chunks by their original chunk number."""

    return sorted(
        records,
        key=lambda record: record["metadata"]["chunk"],
    )


# === Deduplicate Chunks ===

def deduplicate_chunks(
    records: list[dict],
) -> list[dict]:
    """Removes duplicate chunks using their IDs."""

    seen = set()

    unique_records = []

    for record in records:

        record_id = record["id"]

        if record_id in seen:
            continue

        seen.add(record_id)

        unique_records.append(
            record
        )

    return unique_records


# === Assemble Context ===

def assemble_context(
    records: list[dict],
) -> str:
    """Combines retrieved chunks into a single context string."""

    sections = []

    for record in records:

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


# === Process Retrieved Chunks ===

selected_chunks = select_chunks(
    records,
    TOP_K,
)

print("\n=== Selected Chunks ===")

for record in selected_chunks:

    print(
        f"ID: {record['id']}"
    )


ordered_chunks = order_chunks(
    selected_chunks
)

print("\n=== Ordered Chunks ===")

for record in ordered_chunks:

    print(
        f"ID: {record['id']} "
        f"| Chunk: "
        f"{record['metadata']['chunk']}"
    )


unique_chunks = deduplicate_chunks(
    ordered_chunks
)

print("\n=== Deduplicated Chunks ===")

for record in unique_chunks:

    print(
        f"ID: {record['id']}"
    )


# === Build Context ===

context = assemble_context(
    unique_chunks
)

print("\n=== Assembled Context ===")

print(context)
