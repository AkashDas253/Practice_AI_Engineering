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


def load_txt(file_path: Path) -> bytes:
    """Loads a TXT file as raw bytes."""

    return file_path.read_bytes()


print("\n=== TXT ===")

txt_files = discover_txt_files(PATH)

print(
    f"[Discovered] {len(txt_files)} TXT file(s)"
)

for file_path in txt_files:

    content = load_txt(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )


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


def load_markdown(file_path: Path) -> bytes:
    """Loads a Markdown file as raw bytes."""

    return file_path.read_bytes()


print("\n=== Markdown ===")

markdown_files = discover_markdown_files(PATH)

print(
    f"[Discovered] "
    f"{len(markdown_files)} Markdown file(s)"
)

for file_path in markdown_files:

    content = load_markdown(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )


# === JSON ===

from pathlib import Path


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


def load_json(file_path: Path) -> bytes:
    """Loads a JSON file as raw bytes."""

    return file_path.read_bytes()


print("\n=== JSON ===")

json_files = discover_json_files(PATH)

print(
    f"[Discovered] {len(json_files)} JSON file(s)"
)

for file_path in json_files:

    content = load_json(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )


# === CSV ===

from pathlib import Path


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


def load_csv(file_path: Path) -> bytes:
    """Loads a CSV file as raw bytes."""

    return file_path.read_bytes()


print("\n=== CSV ===")

csv_files = discover_csv_files(PATH)

print(
    f"[Discovered] {len(csv_files)} CSV file(s)"
)

for file_path in csv_files:

    content = load_csv(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )


# === HTML ===

from pathlib import Path


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


def load_html(file_path: Path) -> bytes:
    """Loads an HTML file as raw bytes."""

    return file_path.read_bytes()


print("\n=== HTML ===")

html_files = discover_html_files(PATH)

print(
    f"[Discovered] {len(html_files)} HTML file(s)"
)

for file_path in html_files:

    content = load_html(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )


# === PDF ===

from pathlib import Path


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


def load_pdf(file_path: Path) -> bytes:
    """Loads a PDF file as raw bytes."""

    return file_path.read_bytes()


print("\n=== PDF ===")

pdf_files = discover_pdf_files(PATH)

print(
    f"[Discovered] {len(pdf_files)} PDF file(s)"
)

for file_path in pdf_files:

    content = load_pdf(file_path)

    print(
        f"[Loaded] {file_path.name}"
    )

    print(
        f"[Type] {file_path.suffix.lower()}"
    )

    print(
        f"[Size] {len(content)} bytes"
    )
