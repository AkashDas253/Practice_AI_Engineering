import logging
import time


# Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

MAX_RETRIES = 3


# Example operation

attempt_count = 0


def model_operation() -> str:
    """Simulates an operation that succeeds after retries."""

    global attempt_count

    attempt_count += 1

    if attempt_count < 3:
        raise RuntimeError("Temporary model error")

    return "Model request completed successfully"


# Run operation with retries

print("=== Retry Tracking ===")

retry_count = 0
retry_reasons = []
final_result = None
final_error = None

while retry_count <= MAX_RETRIES:

    attempt_number = retry_count + 1

    logging.info(
        "Attempt started | attempt=%s",
        attempt_number,
    )

    try:
        final_result = model_operation()

        logging.info(
            "Attempt completed | attempt=%s | result=%s",
            attempt_number,
            final_result,
        )

        break

    except Exception as error:

        retry_reasons.append(str(error))

        logging.error(
            "Attempt failed | attempt=%s | error=%s",
            attempt_number,
            error,
        )

        if retry_count >= MAX_RETRIES:

            final_error = str(error)

            logging.error(
                "Retries exhausted | attempts=%s",
                attempt_number,
            )

            break

        retry_count += 1

        logging.info(
            "Retry scheduled | retry=%s | reason=%s",
            retry_count,
            error,
        )

        time.sleep(0.1)


# Summary

total_attempts = attempt_count
successful = final_result is not None
retries_used = max(total_attempts - 1, 0)

print("\n=== Retry Summary ===")
print(f"Total attempts:  {total_attempts}")
print(f"Retries used:    {retries_used}")
print(f"Max retries:     {MAX_RETRIES}")
print(f"Final outcome:   {'success' if successful else 'failed'}")

if retry_reasons:
    print("\nRetry reasons:")

    for number, reason in enumerate(
        retry_reasons,
        start=1,
    ):
        print(f"{number}. {reason}")

if final_error is not None:
    print(f"\nFinal error: {final_error}")
