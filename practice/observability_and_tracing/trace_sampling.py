import logging
import random
import uuid

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def should_sample(sample_rate):
    # Randomly decide whether this trace should be recorded.
    return random.random() < sample_rate


def process_trace(trace_number, sample_rate):
    trace_id = str(uuid.uuid4())

    sampled = should_sample(sample_rate)

    if sampled:
        logger.info(
            "Trace recorded | trace_id=%s | trace_number=%s",
            trace_id,
            trace_number,
        )

        return {
            "trace_id": trace_id,
            "trace_number": trace_number,
            "sampled": True,
        }

    logger.info(
        "Trace skipped | trace_id=%s | trace_number=%s",
        trace_id,
        trace_number,
    )

    return {
        "trace_id": trace_id,
        "trace_number": trace_number,
        "sampled": False,
    }


if __name__ == "__main__":
    print("=== Trace Sampling ===")

    total_traces = 10
    sample_rate = 0.30

    print(f"Total traces: {total_traces}")
    print(f"Sample rate: {sample_rate * 100:.0f}%")

    results = []

    for trace_number in range(1, total_traces + 1):
        result = process_trace(trace_number, sample_rate)
        results.append(result)

    sampled_count = sum(
        1 for result in results if result["sampled"]
    )

    skipped_count = total_traces - sampled_count

    print("\n=== Sampling Summary ===")
    print(f"Total traces:    {total_traces}")
    print(f"Recorded traces: {sampled_count}")
    print(f"Skipped traces:  {skipped_count}")
    print(
        f"Actual sample rate: "
        f"{(sampled_count / total_traces) * 100:.1f}%"
    )
