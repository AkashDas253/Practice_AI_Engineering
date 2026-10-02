import logging
import statistics

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def collect_trace_data():
    # Simulate traces that were collected by the application.
    return [
        {
            "trace_id": "trace-001",
            "latency": 2.4,
            "tokens": 420,
            "tool_calls": 1,
            "success": True,
        },
        {
            "trace_id": "trace-002",
            "latency": 3.1,
            "tokens": 560,
            "tool_calls": 2,
            "success": True,
        },
        {
            "trace_id": "trace-003",
            "latency": 1.8,
            "tokens": 310,
            "tool_calls": 1,
            "success": True,
        },
        {
            "trace_id": "trace-004",
            "latency": 4.2,
            "tokens": 690,
            "tool_calls": 2,
            "success": False,
        },
        {
            "trace_id": "trace-005",
            "latency": 2.7,
            "tokens": 480,
            "tool_calls": 1,
            "success": True,
        },
    ]


def calculate_metrics(traces):
    total_requests = len(traces)

    successful_requests = sum(
        1 for trace in traces if trace["success"]
    )

    failed_requests = total_requests - successful_requests

    latencies = [trace["latency"] for trace in traces]

    total_tokens = sum(
        trace["tokens"] for trace in traces
    )

    total_tool_calls = sum(
        trace["tool_calls"] for trace in traces
    )

    return {
        "total_requests": total_requests,
        "successful_requests": successful_requests,
        "failed_requests": failed_requests,
        "success_rate": (
            successful_requests / total_requests * 100
            if total_requests
            else 0
        ),
        "average_latency": statistics.mean(latencies),
        "max_latency": max(latencies),
        "total_tokens": total_tokens,
        "average_tokens": (
            total_tokens / total_requests
            if total_requests
            else 0
        ),
        "total_tool_calls": total_tool_calls,
    }


if __name__ == "__main__":
    print("=== Observability Dashboard Data ===")

    traces = collect_trace_data()

    logger.info(
        "Collected traces | count=%s",
        len(traces),
    )

    metrics = calculate_metrics(traces)

    logger.info(
        "Metrics calculated | requests=%s | failures=%s",
        metrics["total_requests"],
        metrics["failed_requests"],
    )

    print("\n=== Metrics ===")
    print(f"Total requests:       {metrics['total_requests']}")
    print(f"Successful requests:  {metrics['successful_requests']}")
    print(f"Failed requests:      {metrics['failed_requests']}")
    print(f"Success rate:         {metrics['success_rate']:.1f}%")
    print(f"Average latency:      {metrics['average_latency']:.2f}s")
    print(f"Maximum latency:      {metrics['max_latency']:.2f}s")
    print(f"Total tokens:         {metrics['total_tokens']}")
    print(f"Average tokens:       {metrics['average_tokens']:.1f}")
    print(f"Total tool calls:     {metrics['total_tool_calls']}")
