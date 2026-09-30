import os
import json
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# === Config ===

BASE_PATH = Path(__file__).resolve().parent

STORE_PATH = (
    BASE_PATH
    / "output"
    / "vector_store.json"
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

TOP_K = 3


# === Conversation ===

conversation = [
    {
        "role": "user",
        "content": (
            "What is retrieval-augmented generation?"
        ),
    },
    {
        "role": "assistant",
        "content": (
            "RAG combines information retrieval "
            "with language generation."
        ),
    },
    {
        "role": "user",
        "content": (
            "How does it use that information?"
        ),
    },
]


# === Load Vector Store ===

def load_vector_store(
    store_path: Path,
) -> list[dict]:
    """Loads vector records from JSON."""

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


# === Display Conversation ===

def display_conversation(
    messages: list[dict],
) -> None:
    """Displays the conversation."""

    print("\n=== Conversation ===")

    for message in messages:

        print(
            f"{message['role'].title()}: "
            f"{message['content']}"
        )


display_conversation(
    conversation
)


# === Build Retrieval Query ===

def build_retrieval_query(
    messages: list[dict],
) -> str:
    """Builds a standalone retrieval query from conversation context."""

    conversation_text = "\n".join(
        f"{message['role']}: "
        f"{message['content']}"
        for message in messages
    )

    prompt = f"""
Convert the following conversation into one
standalone search query.

Resolve references such as "it", "that", or
"this" using the previous conversation.

Return only the search query.
Do not answer it.

Conversation:
{conversation_text}
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text.strip()


retrieval_query = build_retrieval_query(
    conversation
)


# === Generate Embedding ===

def generate_embedding(
    text: str,
) -> list[float]:
    """Generates an embedding for text."""

    response = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    return response.embeddings[0].values


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


# === Retrieve Documents ===

def retrieve_documents(
    query: str,
    documents: list[dict],
    top_k: int,
) -> list[dict]:
    """Retrieves the most relevant documents."""

    query_embedding = generate_embedding(
        query
    )

    scored_documents = []

    for document in documents:

        score = cosine_similarity(
            query_embedding,
            document["embedding"],
        )

        scored_documents.append(
            (
                score,
                document,
            )
        )

    scored_documents.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [
        {
            **document,
            "similarity": score,
        }
        for score, document
        in scored_documents[:top_k]
    ]


retrieved_documents = retrieve_documents(
    retrieval_query,
    records,
    TOP_K,
)


# === Build Context ===

def build_context(
    documents: list[dict],
) -> str:
    """Builds context from retrieved documents."""

    sections = []

    for document in documents:

        metadata = document["metadata"]

        sections.append(
            (
                f"[Source: {metadata['source']} | "
                f"Chunk: {metadata['chunk']}]\n"
                f"{document['text']}"
            )
        )

    return "\n\n".join(
        sections
    )


context = build_context(
    retrieved_documents
)


# === Generate Answer ===

def generate_answer(
    messages: list[dict],
    context: str,
) -> str:
    """Generates an answer using conversation and retrieved context."""

    conversation_text = "\n".join(
        f"{message['role']}: "
        f"{message['content']}"
        for message in messages
    )

    prompt = f"""
Answer the user's latest question using the
retrieved context below.

Use the conversation to understand references
and follow-up questions.

Do not introduce information that is not
supported by the retrieved context.

Conversation:
{conversation_text}

Retrieved context:
{context}

Answer:
"""

    response = client.models.generate_content(
        model=GENERATION_MODEL,
        contents=prompt,
    )

    return response.text.strip()


# === Output ===

print("\n=== Retrieval Query ===")

print(retrieval_query)

print("\n=== Retrieved Documents ===")

for index, document in enumerate(
    retrieved_documents,
    start=1,
):

    metadata = document["metadata"]

    print(
        f"\n[Result {index}]"
    )

    print(
        f"ID: {document['id']}"
    )

    print(
        f"Similarity: "
        f"{document['similarity']:.4f}"
    )

    print(
        f"Source: {metadata['source']}"
    )

    print(
        f"Chunk: {metadata['chunk']}"
    )


print("\n=== Context ===")

print(context)

print("\n=== Generating Answer ===")

answer = generate_answer(
    conversation,
    context,
)

print("\n=== RAG Answer ===")

print(answer)
