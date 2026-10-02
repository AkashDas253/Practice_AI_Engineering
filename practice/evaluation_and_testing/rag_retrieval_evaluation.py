import re


# Sample documents

documents = [
    {
        "id": "doc_1",
        "title": "Python",
        "text": (
            "Python is a high-level programming language "
            "known for its simple syntax and readability."
        ),
    },
    {
        "id": "doc_2",
        "title": "JavaScript",
        "text": (
            "JavaScript is a programming language commonly "
            "used to create interactive web pages."
        ),
    },
    {
        "id": "doc_3",
        "title": "Machine Learning",
        "text": (
            "Machine learning is a branch of artificial intelligence "
            "that allows systems to learn patterns from data."
        ),
    },
    {
        "id": "doc_4",
        "title": "RAG",
        "text": (
            "Retrieval-augmented generation combines document retrieval "
            "with language model generation."
        ),
    },
]


# Simulated retrieval

def retrieve_documents(query: str) -> list[dict]:
    """Returns documents that match important query words."""

    query_words = set(
        re.findall(r"\b[a-zA-Z]+\b", query.lower())
    )

    scored_documents = []

    for document in documents:

        document_text = (
            document["title"] + " " + document["text"]
        ).lower()

        document_words = set(
            re.findall(r"\b[a-zA-Z]+\b", document_text)
        )

        score = len(query_words & document_words)

        if score > 0:
            scored_documents.append(
                {
                    "document": document,
                    "score": score,
                }
            )

    scored_documents.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    return [
        item["document"]
        for item in scored_documents
    ]


# Retrieval evaluation

def evaluate_retrieval(
    retrieved_documents: list[dict],
    expected_document_ids: list[str],
) -> tuple[bool, list[str]]:

    issues = []

    retrieved_ids = [
        document["id"]
        for document in retrieved_documents
    ]

    # Check that expected documents were retrieved

    for expected_id in expected_document_ids:

        if expected_id not in retrieved_ids:
            issues.append(
                f"Expected document was not retrieved: {expected_id}"
            )

    # Check for unexpected empty retrieval

    if not retrieved_documents:
        issues.append(
            "Retriever returned no documents."
        )

    # Check that enough relevant documents were retrieved

    relevant_count = sum(
        1
        for document_id in retrieved_ids
        if document_id in expected_document_ids
    )

    if expected_document_ids:

        relevance_ratio = (
            relevant_count
            / len(expected_document_ids)
        )

        if relevance_ratio < 1.0:
            issues.append(
                "Retrieval did not return all expected "
                "relevant documents."
            )

    return len(issues) == 0, issues


# Test cases

test_cases = [
    {
        "name": "Python Query",
        "query": "What is Python?",
        "expected_document_ids": ["doc_1"],
    },
    {
        "name": "Machine Learning Query",
        "query": "What is machine learning?",
        "expected_document_ids": ["doc_3"],
    },
    {
        "name": "RAG Query",
        "query": "What is retrieval augmented generation?",
        "expected_document_ids": ["doc_4"],
    },
]


# Run evaluation

print("=== RAG Retrieval Evaluation ===")
print(f"Documents: {len(documents)}")
print(f"Test cases: {len(test_cases)}")


total = 0
passed = 0
failed = 0


for test_case in test_cases:

    print(
        f"\n--- Test: {test_case['name']} ---"
    )

    query = test_case["query"]
    expected_ids = test_case["expected_document_ids"]

    print(f"[Query] {query}")
    print(
        f"[Expected Documents] "
        f"{expected_ids}"
    )

    retrieved_documents = retrieve_documents(query)

    retrieved_ids = [
        document["id"]
        for document in retrieved_documents
    ]

    print(
        f"[Retrieved Documents] "
        f"{retrieved_ids}"
    )

    for document in retrieved_documents:

        print(
            f"[Retrieved] "
            f"{document['id']} - "
            f"{document['title']}"
        )

    result, issues = evaluate_retrieval(
        retrieved_documents,
        expected_ids,
    )

    if result:

        print("[Result] PASS")
        print(
            "[Evaluation] Retrieval returned "
            "the expected relevant documents."
        )

        passed += 1

    else:

        print("[Result] FAIL")
        print(
            "[Evaluation] Retrieval evaluation failed."
        )

        for issue in issues:
            print(f"[Issue] {issue}")

        failed += 1

    total += 1


# Summary

print("\n=== RAG Retrieval Evaluation Summary ===")

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
