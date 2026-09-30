from pathlib import Path
import re


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"

SOURCE_FILE = PATH / "rag.txt"


# === Load Source Text ===

from pathlib import Path


def load_source_text(file_path: Path) -> str:
    """Loads the source document as text."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


text = load_source_text(SOURCE_FILE)

print("=== Source Document ===")
print(f"Source: {SOURCE_FILE.name}")
print(f"Characters: {len(text)}")


# === Fixed-Size Chunking ===

def fixed_size_chunks(
    text: str,
    chunk_size: int = 200,
) -> list[str]:
    """Splits text into fixed-size character chunks."""

    return [
        text[index:index + chunk_size].strip()
        for index in range(
            0,
            len(text),
            chunk_size,
        )
        if text[index:index + chunk_size].strip()
    ]


chunks = fixed_size_chunks(
    text,
    chunk_size=200,
)

print("\n=== Fixed-Size Chunking ===")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n[Chunk {index}]")
    print(chunk)


# === Sentence-Based Chunking ===

def sentence_chunks(
    text: str,
    sentences_per_chunk: int = 3,
) -> list[str]:
    """Groups sentences into chunks."""

    sentences = [
        sentence.strip()
        for sentence in re.split(
            r"(?<=[.!?])\s+",
            text,
        )
        if sentence.strip()
    ]

    chunks = []

    for index in range(
        0,
        len(sentences),
        sentences_per_chunk,
    ):

        chunk = " ".join(
            sentences[
                index:index + sentences_per_chunk
            ]
        )

        if chunk:
            chunks.append(chunk)

    return chunks


chunks = sentence_chunks(
    text,
    sentences_per_chunk=3,
)

print("\n=== Sentence-Based Chunking ===")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n[Chunk {index}]")
    print(chunk)


# === Paragraph-Based Chunking ===

def paragraph_chunks(
    text: str,
) -> list[str]:
    """Splits text into paragraph-based chunks."""

    paragraphs = re.split(
        r"\n\s*\n",
        text,
    )

    return [
        paragraph.strip()
        for paragraph in paragraphs
        if paragraph.strip()
    ]


chunks = paragraph_chunks(text)

print("\n=== Paragraph-Based Chunking ===")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n[Chunk {index}]")
    print(chunk)


# === Recursive Chunking ===

def recursive_chunks(
    text: str,
    chunk_size: int = 300,
) -> list[str]:
    """Splits text using progressively smaller separators."""

    separators = [
        "\n\n",
        "\n",
        ". ",
        " ",
    ]

    def split_text(
        value: str,
        separator_index: int = 0,
    ) -> list[str]:

        if len(value) <= chunk_size:
            return [value.strip()]

        if separator_index >= len(separators):
            return [
                value[index:index + chunk_size].strip()
                for index in range(
                    0,
                    len(value),
                    chunk_size,
                )
                if value[index:index + chunk_size].strip()
            ]

        separator = separators[separator_index]

        parts = [
            part.strip()
            for part in value.split(separator)
            if part.strip()
        ]

        chunks = []
        current = ""

        for part in parts:

            candidate = (
                f"{current}{separator}{part}"
                if current
                else part
            )

            if len(candidate) <= chunk_size:

                current = candidate

            else:

                if current:
                    chunks.extend(
                        split_text(
                            current,
                            separator_index + 1,
                        )
                    )

                current = part

        if current:
            chunks.extend(
                split_text(
                    current,
                    separator_index + 1,
                )
            )

        return chunks

    return split_text(text)


chunks = recursive_chunks(
    text,
    chunk_size=300,
)

print("\n=== Recursive Chunking ===")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n[Chunk {index}]")
    print(chunk)


# === Overlapping Chunks ===

def overlapping_chunks(
    text: str,
    chunk_size: int = 200,
    overlap: int = 50,
) -> list[str]:
    """Creates fixed-size chunks with overlapping content."""

    if overlap >= chunk_size:
        raise ValueError(
            "overlap must be smaller than chunk_size"
        )

    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        chunk = text[start:end].strip()

        if chunk:
            chunks.append(chunk)

        if end >= len(text):
            break

        start = end - overlap

    return chunks


chunks = overlapping_chunks(
    text,
    chunk_size=200,
    overlap=50,
)

print("\n=== Overlapping Chunks ===")

for index, chunk in enumerate(chunks, start=1):

    print(f"\n[Chunk {index}]")
    print(chunk)


