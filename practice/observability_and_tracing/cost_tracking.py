import logging


# Configuration

MODEL = "models/gemini-3.5-flash-lite"

INPUT_COST_PER_1M_TOKENS = 0.10
OUTPUT_COST_PER_1M_TOKENS = 0.40


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# Cost calculation

def calculate_cost(
    input_tokens: int,
    output_tokens: int,
) -> dict:

    input_cost = (
        input_tokens / 1_000_000
    ) * INPUT_COST_PER_1M_TOKENS

    output_cost = (
        output_tokens / 1_000_000
    ) * OUTPUT_COST_PER_1M_TOKENS

    total_cost = input_cost + output_cost

    return {
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "total_tokens": input_tokens + output_tokens,
        "input_cost": input_cost,
        "output_cost": output_cost,
        "total_cost": total_cost,
    }


# Simulated tracked usage

usage = [
    {
        "request": 1,
        "input_tokens": 800,
        "output_tokens": 1200,
    },
    {
        "request": 2,
        "input_tokens": 1500,
        "output_tokens": 900,
    },
]


# Track request costs

print("=== Cost Tracking ===")
print(f"Model: {MODEL}")
print(
    f"Input cost per 1M tokens: "
    f"${INPUT_COST_PER_1M_TOKENS:.2f}"
)
print(
    f"Output cost per 1M tokens: "
    f"${OUTPUT_COST_PER_1M_TOKENS:.2f}"
)

total_input_tokens = 0
total_output_tokens = 0
total_cost = 0.0


for request in usage:

    logging.info(
        "Calculating request cost | request=%s",
        request["request"],
    )

    cost = calculate_cost(
        request["input_tokens"],
        request["output_tokens"],
    )

    total_input_tokens += cost["input_tokens"]
    total_output_tokens += cost["output_tokens"]
    total_cost += cost["total_cost"]

    print(f"\n--- Request {request['request']} ---")
    print(f"Input tokens:  {cost['input_tokens']}")
    print(f"Output tokens: {cost['output_tokens']}")
    print(f"Total tokens:  {cost['total_tokens']}")
    print(f"Input cost:    ${cost['input_cost']:.8f}")
    print(f"Output cost:   ${cost['output_cost']:.8f}")
    print(f"Request cost:  ${cost['total_cost']:.8f}")


# Summary

print("\n=== Cost Summary ===")
print(f"Input tokens:  {total_input_tokens}")
print(f"Output tokens: {total_output_tokens}")
print(
    f"Total tokens:  "
    f"{total_input_tokens + total_output_tokens}"
)
print(f"Total cost:    ${total_cost:.8f}")

logging.info(
    "Cost tracking completed | total_tokens=%s | total_cost=$%.8f",
    total_input_tokens + total_output_tokens,
    total_cost,
)
