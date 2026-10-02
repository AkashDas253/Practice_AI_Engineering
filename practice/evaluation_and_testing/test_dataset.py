# === Test Dataset ===

test_dataset = [
    {
        "name": "Simple Arithmetic",
        "prompt": "What is 2 + 2?",
        "expected": "4",
    },
    {
        "name": "Capital City",
        "prompt": "What is the capital of France?",
        "expected": "Paris",
    },
    {
        "name": "Programming Language",
        "prompt": "Is Python a programming language?",
        "expected": "Yes",
    },
]


# === Dataset Information ===

print("=== Test Dataset ===")
print(f"Test cases: {len(test_dataset)}")


# === Display Test Cases ===

for index, test_case in enumerate(test_dataset, start=1):

    print(f"\n--- Test {index}: {test_case['name']} ---")

    print(f"[Prompt]   {test_case['prompt']}")
    print(f"[Expected] {test_case['expected']}")


# === Dataset Fields ===

print("\n=== Dataset Structure ===")

for index, test_case in enumerate(test_dataset, start=1):

    print(f"\n--- Test {index} ---")

    print(f"Name:     {test_case['name']}")
    print(f"Prompt:   {test_case['prompt']}")
    print(f"Expected: {test_case['expected']}")


# === Reusable Dataset Access ===

print("\n=== Dataset Access ===")

first_test = test_dataset[0]

print(f"Name:     {first_test['name']}")
print(f"Prompt:   {first_test['prompt']}")
print(f"Expected: {first_test['expected']}")
