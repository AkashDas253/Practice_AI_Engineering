from pathlib import Path


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"

SOURCE_FILE = PATH / "rag.txt"


# === Document Metadata ===

from pathlib import Path


def extract_document_metadata(
    file_path: Path,
) -> dict:
    """Extracts basic metadata from a document."""

    return {
        "source": file_path.name,
        "title": file_path.stem,
        "document_type": file_path.suffix.lower(),
    }


document_metadata = extract_document_metadata(
    SOURCE_FILE
)

print("=== Document Metadata ===")

for key, value in document_metadata.items():
    print(f"{key}: {value}")


# === Section Metadata ===

def extract_section_metadata(
    text: str,
) -> list[dict]:
    """Extracts metadata for document sections."""

    sections = [
        section.strip()
        for section in text.split("\n\n")
        if section.strip()
    ]

    metadata = []

    for index, section in enumerate(
        sections,
        start=1,
    ):

        metadata.append(
            {
                "section": index,
                "text": section,
            }
        )

    return metadata


text = SOURCE_FILE.read_text(
    encoding="utf-8"
)

sections = extract_section_metadata(text)

print("\n=== Section Metadata ===")

for section in sections:

    print(
        f"\nSection: "
        f"{section['section']}"
    )

    print(
        f"Characters: "
        f"{len(section['text'])}"
    )


# === Chunk Metadata ===

def attach_chunk_metadata(
    chunks: list[str],
    document_metadata: dict,
) -> list[dict]:
    """Attaches metadata to document chunks."""

    results = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        results.append(
            {
                "source": document_metadata["source"],
                "title": document_metadata["title"],
                "document_type": document_metadata["document_type"],
                "chunk": index,
                "text": chunk,
            }
        )

    return results


chunks = [
    text[index:index + 200].strip()
    for index in range(
        0,
        len(text),
        200,
    )
    if text[index:index + 200].strip()
]

chunk_records = attach_chunk_metadata(
    chunks,
    document_metadata,
)

print("\n=== Chunk Metadata ===")

for record in chunk_records:

    print(
        f"\nSource: "
        f"{record['source']}"
    )

    print(
        f"Title: "
        f"{record['title']}"
    )

    print(
        f"Document Type: "
        f"{record['document_type']}"
    )

    print(
        f"Chunk: "
        f"{record['chunk']}"
    )

    print(
        f"Characters: "
        f"{len(record['text'])}"
    )


# === Combined Metadata ===

def build_document_records(
    file_path: Path,
) -> list[dict]:
    """Builds retrieval-ready records with metadata."""

    document_metadata = extract_document_metadata(
        file_path
    )

    text = file_path.read_text(
        encoding="utf-8"
    )

    chunks = [
        text[index:index + 200].strip()
        for index in range(
            0,
            len(text),
            200,
        )
        if text[index:index + 200].strip()
    ]

    records = []

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        records.append(
            {
                **document_metadata,
                "chunk": index,
                "text": chunk,
            }
        )

    return records


records = build_document_records(
    SOURCE_FILE
)

print("\n=== Retrieval Records ===")

for record in records:

    print(
        f"\n{record}"
    )
