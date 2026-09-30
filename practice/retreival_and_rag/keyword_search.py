import json
import re
from pathlib import Path


# === Config ===

PATH = Path(__file__).resolve().parent

OUTPUT_PATH = PATH / "output"

STORE_PATH = OUTPUT_PATH / "vector_store.json"

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


# === Tokenize Text ===

def tokenize(
    text: str,
) -> list[str]:
    """Converts text into normalized word tokens."""

    return re.findall(
        r"\b[a-zA-Z0-9]+\b",
        text.lower(),
    )


# === Keyword Score ===

def keyword_score(
    query: str,
    text: str,
) -> int:
    """Counts matching query keywords in document text."""

    query_words = set(
        tokenize(query)
    )

    text_words = set(
        tokenize(text)
    )

    return len(
        query_words.intersection(
            text_words
        )
    )


# === Score Records ===

def score_records(
    query: str,
    records: list[dict],
) -> list[dict]:
    """Calculates keyword scores for each record."""

    scored_records = []

    for record in records:

        score = keyword_score(
            query,
            record["text"],
        )

        scored_records.append(
            {
                **record,
                "keyword_score": score,
            }
        )

    return scored_records


# === Top-K Selection ===

def select_top_k(
    records: list[dict],
    top_k: int,
) -> list[dict]:
    """Returns the highest-scoring records."""

    sorted_records = sorted(
        records,
        key=lambda record: record["keyword_score"],
        reverse=True,
    )

    return sorted_records[:top_k]


# === Search ===

def keyword_search(
    query: str,
    records: list[dict],
    top_k: int = 3,
) -> list[dict]:
    """Performs keyword-based retrieval."""

    scored_records = score_records(
        query,
        records,
    )

    return select_top_k(
        scored_records,
        top_k,
    )


# === Query ===

query = (
    "How does retrieval augmented generation "
    "use retrieved information?"
)

print("\n=== Query ===")

print(query)

print(
    f"\nTop-K: {TOP_K}"
)


# === Search ===

results = keyword_search(
    query,
    records,
    top_k=TOP_K,
)


# === Results ===

print("\n=== Keyword Search Results ===")

for index, result in enumerate(
    results,
    start=1,
):

    print(
        f"\n[Result {index}]"
    )

    print(
        f"ID: {result['id']}"
    )

    print(
        f"Keyword Score: "
        f"{result['keyword_score']}"
    )

    print(
        f"Source: "
        f"{result['metadata']['source']}"
    )

    print(
        f"Chunk: "
        f"{result['metadata']['chunk']}"
    )

    print(
        f"Text: "
        f"{result['text']}"
    )


# === Comparison ===

print("\n=== Retrieval Comparison ===")

print(
    "Keyword search uses exact word overlap."
)

print(
    "Semantic search uses embedding similarity."
)

print(
    "Keyword search can miss related concepts "
    "when different words are used."
)
