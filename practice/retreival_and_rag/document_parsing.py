from pathlib import Path


# === Config ===

PATH = Path(__file__).resolve().parent / "documents"


# === TXT ===

from pathlib import Path


def discover_txt_files(path: Path) -> list[Path]:
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


def parse_txt(file_path: Path) -> str:
    """Extracts usable text from a TXT file."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


print("\n=== TXT ===")

txt_files = discover_txt_files(PATH)

for file_path in txt_files:

    text = parse_txt(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")


# === Markdown ===

from pathlib import Path


def discover_markdown_files(path: Path) -> list[Path]:
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


def parse_markdown(file_path: Path) -> str:
    """Extracts usable text from a Markdown file."""

    return file_path.read_text(
        encoding="utf-8"
    ).strip()


print("\n=== Markdown ===")

markdown_files = discover_markdown_files(PATH)

for file_path in markdown_files:

    text = parse_markdown(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")


# === JSON ===

from pathlib import Path
import json


def discover_json_files(path: Path) -> list[Path]:
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


def parse_json(file_path: Path) -> str:
    """Extracts usable text from JSON data."""

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

    text = parse_json(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")


# === CSV ===

from pathlib import Path
import csv


def discover_csv_files(path: Path) -> list[Path]:
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


def parse_csv(file_path: Path) -> str:
    """Extracts usable text from CSV rows."""

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

    text = parse_csv(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")


# === HTML ===

from pathlib import Path
from html.parser import HTMLParser


def discover_html_files(path: Path) -> list[Path]:
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

    def handle_data(self, data: str):
        text = data.strip()

        if text:
            self.parts.append(text)


def parse_html(file_path: Path) -> str:
    """Extracts usable text from an HTML file."""

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

    text = parse_html(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")


# === PDF ===

from pathlib import Path
from pypdf import PdfReader


def discover_pdf_files(path: Path) -> list[Path]:
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


def parse_pdf(file_path: Path) -> str:
    """Extracts text from a PDF file."""

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

    text = parse_pdf(file_path)

    print(f"[Parsed] {file_path.name}")
    print(f"[Characters] {len(text)}")
    print(f"[Text]\n{text}")
