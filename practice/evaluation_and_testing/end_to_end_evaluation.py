import os
from pathlib import Path

from dotenv import load_dotenv
from google import genai
from google.genai import types


# Config

env_path = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set in .env")

client = genai.Client(api_key=api_key)

model = "models/gemini-3.5-flash-lite"


# Knowledge base

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
            "used for web development."
        ),
    },
    "doc_3": {
        "title": "Machine Learning",
        "content": (
            "Machine learning is a branch of artificial "
            "intelligence that enables systems to learn "
            "patterns from data."
        ),
    },
}


# Retrieval

def retrieve_documents(query: str) -> list[dict]:
    """Returns documents relevant to the query."""

    query_lower = query.lower()

    results = []

    if "python" in query_lower:
        results.append(documents["doc_1"])

    if "javascript" in query_lower:
        results.append(documents["doc_2"])

    if "machine learning" in query_lower:
        results.append(documents["doc_3"])

    return results


# Tool

def calculate(expression: str) -> dict:
    """Calculates a simple arithmetic expression."""

    try:
        result = eval(
            expression,
            {"__builtins__": {}},
            {},
        )

        return {
            "expression": expression,
            "result": result,
        }

    except Exception as error:
        return {
            "expression": expression,
            "error": str(error),
        }


available_tools = {
    "calculate": calculate,
}


calculate_declaration = types.FunctionDeclaration(
    name="calculate",
    description="Calculates a basic arithmetic expression.",
    parameters={
        "type": "OBJECT",
        "properties": {
            "expression": {
                "type": "STRING",
                "description": "A simple arithmetic expression.",
            }
        },
        "required": ["expression"],
    },
)


tools = [
    types.Tool(
        function_declarations=[
            calculate_declaration,
        ]
    )
]


# Model pipeline

def run_pipeline(
    query: str,
    retrieved_documents: list[dict],
) -> tuple[str, str | None]:

    if retrieved_documents:

        context = "\n".join(
            document["content"]
            for document in retrieved_documents
        )

        prompt = (
            "Answer the user's question using the retrieved "
            "context. Do not invent information.\n\n"
            f"Retrieved context:\n{context}\n\n"
            f"User question: {query}"
        )

    else:

        prompt = (
            "Answer the user's question using the available "
            "calculation tool when necessary.\n\n"
            f"User question: {query}"
        )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part(text=prompt)
            ],
        )
    ]

    try:

        while True:

            response = client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    tools=tools,
                    automatic_function_calling=types.AutomaticFunctionCallingConfig(
                        disable=True
                    ),
                ),
            )

            candidate = response.candidates[0]

            function_calls = [
                part.function_call
                for part in candidate.content.parts
                if part.function_call
            ]

            # No tool call means the model has finished.

            if not function_calls:

                return response.text.strip(), None

            contents.append(candidate.content)

            # Execute requested tools.

            for function_call in function_calls:

                tool_name = function_call.name
                arguments = dict(function_call.args)

                if tool_name not in available_tools:
                    return (
                        "",
                        f"Unknown tool requested: {tool_name}",
                    )

                tool_result = available_tools[tool_name](
                    **arguments
                )

                function_response = (
                    types.Part.from_function_response(
                        name=tool_name,
                        response=tool_result,
                    )
                )

                contents.append(
                    types.Content(
                        role="user",
                        parts=[
                            function_response
                        ],
                    )
                )

    except Exception as error:
        return "", str(error)


# Evaluation cases

test_cases = [
    {
        "name": "Python Knowledge Query",
        "query": "What is Python?",
        "expected_document": "Python",
        "expected_answer": (
            "Python is a high-level programming language"
        ),
    },
    {
        "name": "Machine Learning Query",
        "query": "What is machine learning?",
        "expected_document": "Machine Learning",
        "expected_answer": (
            "Machine learning is a branch of artificial intelligence"
        ),
    },
    {
        "name": "Calculation Query",
        "query": "What is 25 * 4?",
        "expected_document": None,
        "expected_answer": "100",
    },
]


# Run evaluation

print("=== End-to-End Evaluation ===")
print(f"Model: {model}")
print(f"Test cases: {len(test_cases)}")


total = 0
passed = 0
failed = 0


for test_case in test_cases:

    print(f"\n--- Test: {test_case['name']} ---")

    query = test_case["query"]

    print(f"[Input] {query}")

    # Retrieval stage

    retrieved_documents = retrieve_documents(query)

    print("\n[Retrieved Documents]")

    if retrieved_documents:

        for document in retrieved_documents:
            print(
                f"- {document['title']}: "
                f"{document['content']}"
            )

    else:
        print("- None")

    # Model and tool stage

    actual_answer, error = run_pipeline(
        query,
        retrieved_documents,
    )

    if error is not None:

        print("\n[Model Error]")
        print(error)

        print("[Result] FAIL")

        failed += 1
        total += 1

        continue

    print("\n[Model Response]")
    print(actual_answer)

    # Evaluate retrieval

    retrieval_passed = True

    expected_document = test_case["expected_document"]

    if expected_document is not None:

        retrieved_titles = [
            document["title"]
            for document in retrieved_documents
        ]

        retrieval_passed = (
            expected_document in retrieved_titles
        )

    # Evaluate final answer

    answer_passed = (
        test_case["expected_answer"].lower()
        in actual_answer.lower()
    )

    if retrieval_passed and answer_passed:

        print("\n[Result] PASS")
        print(
            "[Evaluation] End-to-end pipeline produced "
            "the expected result."
        )

        passed += 1

    else:

        print("\n[Result] FAIL")

        if not retrieval_passed:
            print(
                "[Evaluation] Expected document was "
                "not retrieved."
            )

        if not answer_passed:
            print(
                "[Evaluation] Final answer did not contain "
                "the expected result."
            )

        failed += 1

    total += 1


# Summary

print("\n=== End-to-End Evaluation Summary ===")

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
