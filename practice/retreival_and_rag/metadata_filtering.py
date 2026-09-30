import json
from pathlib import Path


# === Config ===

PATH = Path(__file__).resolve().parent

OUTPUT_PATH = PATH / "output"

STORE_PATH = OUTPUT_PATH / "vector_store.json"


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


# === Metadata Filter ===

def filter_by_metadata(
    records: list[dict],
    filters: dict,
) -> list[dict]:
    """Returns records matching all metadata filters."""

    filtered_records = []

    for record in records:

        metadata = record.get(
            "metadata",
            {}
        )

        matches = all(
            metadata.get(key) == value
            for key, value in filters.items()
        )

        if matches:
            filtered_records.append(
                record
            )

    return filtered_records


# === Display Records ===

def display_records(
    records: list[dict],
):
    """Displays retrieved records."""

    for index, record in enumerate(
        records,
        start=1,
    ):

        print(
            f"\n[Result {index}]"
        )

        print(
            f"ID: {record['id']}"
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


# === Filter Configuration ===

filters = {
    "document_type": ".txt",
}


# === Apply Filter ===

print("\n=== Metadata Filter ===")

for key, value in filters.items():

    print(
        f"{key}: {value}"
    )


filtered_records = filter_by_metadata(
    records,
    filters,
)


# === Results ===

print("\n=== Filtered Results ===")

print(
    f"Records matched: "
    f"{len(filtered_records)}"
)

display_records(
    filtered_records
)
