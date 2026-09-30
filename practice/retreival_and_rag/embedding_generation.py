import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"

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


# === TXT ===

from pathlib import Path


def discover_txt_files(
    path: Path,
) -> list[Path]:
    """Discovers TXT files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".txt"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


def load_txt(
    file_path: Path,
) -> str:
    """Loads normalized text from a TXT file."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


def chunk_text(
    text: str,
    chunk_size: int = 300,
) -> list[str]:
    """Creates simple fixed-size chunks."""

    return [
        text[index:index + chunk_size].strip()
        for index in range(
            0,
            len(text),
            chunk_size,
        )
        if text[index:index + chunk_size].strip()
    ]


def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=model,
        contents=text,
    )

    return response.embeddings[0].values


print("\n=== TXT ===")

txt_files = discover_txt_files(PATH)

for file_path in txt_files:

    text = load_txt(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )


# === Markdown ===

from pathlib import Path


def discover_markdown_files(
    path: Path,
) -> list[Path]:
    """Discovers Markdown files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".md"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


def load_markdown(
    file_path: Path,
) -> str:
    """Loads normalized text from Markdown."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


print("\n=== Markdown ===")

markdown_files = discover_markdown_files(PATH)

for file_path in markdown_files:

    text = load_markdown(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )


# === JSON ===

from pathlib import Path
import json


def discover_json_files(
    path: Path,
) -> list[Path]:
    """Discovers JSON files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".json"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


def load_json(
    file_path: Path,
) -> str:
    """Loads and normalizes JSON as text."""

    data = json.loads(
        file_path.read_text(
            encoding="utf-8"
        )
    )

    return json.dumps(
        data,
        ensure_ascii=False,
        indent=2,
    )


print("\n=== JSON ===")

json_files = discover_json_files(PATH)

for file_path in json_files:

    text = load_json(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )


# === CSV ===

from pathlib import Path
import csv


def discover_csv_files(
    path: Path,
) -> list[Path]:
    """Discovers CSV files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".csv"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


def load_csv(
    file_path: Path,
) -> str:
    """Loads CSV rows as normalized text."""

    rows = []

    with file_path.open(
        "r",
        encoding="utf-8",
        newline="",
    ) as file:

        reader = csv.DictReader(file)

        for row in reader:

            values = [
                f"{key}: {value}"
                for key, value in row.items()
            ]

            rows.append(
                " | ".join(values)
            )

    return "\n".join(rows).strip()


print("\n=== CSV ===")

csv_files = discover_csv_files(PATH)

for file_path in csv_files:

    text = load_csv(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )


# === HTML ===

from pathlib import Path
from html.parser import HTMLParser


def discover_html_files(
    path: Path,
) -> list[Path]:
    """Discovers HTML files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".html"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


class TextExtractor(HTMLParser):
    """Extracts visible text from HTML."""

    def __init__(self):
        super().__init__()

        self.parts = []

    def handle_data(
        self,
        data: str,
    ):
        text = data.strip()

        if text:
            self.parts.append(text)


def load_html(
    file_path: Path,
) -> str:
    """Loads and extracts usable HTML text."""

    html = file_path.read_text(
        encoding="utf-8"
    )

    parser = TextExtractor()

    parser.feed(html)

    return "\n".join(
        parser.parts
    ).strip()


print("\n=== HTML ===")

html_files = discover_html_files(PATH)

for file_path in html_files:

    text = load_html(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )


# === PDF ===

from pathlib import Path
from pypdf import PdfReader


def discover_pdf_files(
    path: Path,
) -> list[Path]:
    """Discovers PDF files."""

    return sorted(
        [
            file_path
            for file_path in path.iterdir()
            if file_path.is_file()
            and file_path.suffix.lower() == ".pdf"
        ],
        key=lambda file_path: file_path.name.lower(),
    )


def load_pdf(
    file_path: Path,
) -> str:
    """Extracts usable text from a PDF."""

    reader = PdfReader(file_path)

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(
                text.strip()
            )

    return "\n\n".join(
        pages
    ).strip()


print("\n=== PDF ===")

pdf_files = discover_pdf_files(PATH)

for file_path in pdf_files:

    text = load_pdf(file_path)

    chunks = chunk_text(text)

    print(f"\n[Source] {file_path.name}")
    print(f"[Chunks] {len(chunks)}")

    for index, chunk in enumerate(
        chunks,
        start=1,
    ):

        embedding = generate_embedding(
            chunk
        )

        print(
            f"\n[Chunk] {index}"
        )

        print(
            f"[Characters] {len(chunk)}"
        )

        print(
            f"[Embedding Dimensions] "
            f"{len(embedding)}"
        )

        print(
            f"[First 5 Values] "
            f"{embedding[:5]}"
        )
