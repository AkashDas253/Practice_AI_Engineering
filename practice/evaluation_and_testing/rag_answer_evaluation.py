import os
import re
from pathlib import Path

from dotenv import load_dotenv
from google import genai


# Config

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# Documents

documents = {
    "doc_1": {
        "title": "Python",
        "content": (
            "Python is a high-level programming language "
            "known for its simple syntax and readability."
        ),
    },
    "doc_2": {
        "title": "JavaScript",
        "content": (
            "JavaScript is a programming language commonly "
            "used to create interactive web pages."
        ),
    },
    "doc_3": {
        "title": "Machine Learning",
        "content": (
            "Machine learning is a branch of artificial intelligence "
            "that enables systems to learn patterns from data."
        ),
    },
    "doc_4": {
        "title": "RAG",
        "content": (
            "Retrieval augmented generation combines information "
            "retrieval with language generation. Retrieved documents "
            "provide context that can be used to generate an answer."
        ),
    },
}


# Model Call

def call_model(prompt: str) -> tuple[str, str | None]:
    try:
        response = client.models.generate_content(
            model=model,
            contents=prompt,
        )

        return response.text.strip(), None

    except Exception as error:
        return "", str(error)


# Text Normalization

def normalize_text(text: str) -> str:
    text = text.lower()

    text = re.sub(
        r"[^a-z0-9\s]",
        " ",
        text,
    )

    text = " ".join(text.split())

    return text


# Answer Evaluation

def evaluate_answer(
    answer: str,
    expected_answer: str,
    context: str,
) -> bool:
    """
    Passes when the important concepts from the expected
    answer are present in the actual answer and supported
    by the retrieved context.
    """

    normalized_answer = normalize_text(answer)
    normalized_expected = normalize_text(expected_answer)
    normalized_context = normalize_text(context)

    expected_words = normalized_expected.split()

    stop_words = {
        "a",
        "an",
        "the",
        "is",
        "are",
        "of",
        "to",
        "and",
        "that",
        "with",
        "for",
        "in",
        "on",
        "its",
        "it",
    }

    important_words = [
        word
        for word in expected_words
        if word not in stop_words
    ]

    if not important_words:
        return False

    answer_matches = sum(
        word in normalized_answer
        for word in important_words
    )

    context_matches = sum(
        word in normalized_context
        for word in important_words
    )

    answer_coverage = (
        answer_matches / len(important_words)
    )

    context_coverage = (
        context_matches / len(important_words)
    )

    return (
        answer_coverage >= 0.80
        and context_coverage >= 0.80
    )


# Test Cases

test_cases = [
    {
        "name": "Python Answer",
        "query": "What is Python?",
        "retrieved_documents": ["doc_1"],
        "expected_answer": (
            "Python is a high-level programming language"
        ),
    },
    {
        "name": "Machine Learning Answer",
        "query": "What is machine learning?",
        "retrieved_documents": ["doc_3"],
        "expected_answer": (
            "Machine learning is a branch of artificial intelligence"
        ),
    },
    {
        "name": "RAG Answer",
        "query": "What is retrieval augmented generation?",
        "retrieved_documents": ["doc_4"],
        "expected_answer": (
            "Retrieval augmented generation combines "
            "information retrieval with language generation"
        ),
    },
]


# Run Evaluation

print("=== RAG Answer Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")

total = 0
passed = 0
failed = 0


for test_case in test_cases:

    print(f"\n--- Test: {test_case['name']} ---")

    query = test_case["query"]
    retrieved_documents = test_case["retrieved_documents"]
    expected_answer = test_case["expected_answer"]

    context_parts = []

    for document_id in retrieved_documents:

        document = documents.get(document_id)

        if document is None:
            continue

        context_parts.append(
            f"{document['title']}: {document['content']}"
        )

    context = "\n".join(context_parts)

    prompt = f"""
Answer the user's question using only the provided context.

Context:
{context}

Question:
{query}

Give a concise answer.
"""

    print(f"[Query] {query}")
    print(
        f"[Retrieved Documents] "
        f"{retrieved_documents}"
    )
    print(f"[Expected Answer] {expected_answer}")

    answer, error = call_model(prompt)

    if error is not None:

        print("[API Error]")
        print(error)
        print("[Result] FAIL")

        failed += 1
        total += 1
        continue

    print(f"[Actual Answer] {answer}")

    result = evaluate_answer(
        answer,
        expected_answer,
        context,
    )

    if result:
        print("[Result] PASS")
        print(
            "[Evaluation] Answer is supported by "
            "the retrieved context."
        )
        passed += 1

    else:
        print("[Result] FAIL")
        print(
            "[Evaluation] Answer is not sufficiently "
            "supported by the retrieved context."
        )
        failed += 1

    total += 1


# Summary

print("\n=== RAG Answer Evaluation Summary ===")

print(f"Total Tests:   {total}")
print(f"Passed:        {passed}")
print(f"Failed:        {failed}")

if total > 0:
    pass_rate = (passed / total) * 100
else:
    pass_rate = 0.0

print(f"Pass Rate:     {pass_rate:.2f}%")

if failed == 0:
    print("[Overall Result] PASS")
else:
    print("[Overall Result] FAIL")
