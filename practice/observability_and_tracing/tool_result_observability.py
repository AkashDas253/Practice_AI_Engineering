import logging
import time
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def get_weather(city: str) -> dict:
    """Simulate a weather tool."""
    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        }
    }

    if city not in weather_data:
        raise ValueError(f"Weather data not available for {city}")

    return weather_data[city]


def observe_tool_call(tool_name: str, arguments: dict) -> dict:
    """Execute a tool and record its result and metadata."""
    trace_id = str(uuid.uuid4())
    start_time = time.perf_counter()

    logger.info(
        "Tool call started | trace_id=%s | tool=%s | arguments=%s",
        trace_id,
        tool_name,
        arguments,
    )

    try:
        result = get_weather(**arguments)

        latency = time.perf_counter() - start_time

        metadata = {
            "trace_id": trace_id,
            "tool": tool_name,
            "arguments": arguments,
            "result": result,
            "success": True,
            "latency_seconds": round(latency, 4),
        }

        logger.info(
            "Tool call completed | trace_id=%s | tool=%s | "
            "success=%s | latency=%.4f seconds | result=%s",
            trace_id,
            tool_name,
            True,
            latency,
            result,
        )

        return metadata

    except Exception as error:
        latency = time.perf_counter() - start_time

        metadata = {
            "trace_id": trace_id,
            "tool": tool_name,
            "arguments": arguments,
            "result": None,
            "success": False,
            "latency_seconds": round(latency, 4),
            "error": str(error),
        }

        logger.error(
            "Tool call failed | trace_id=%s | tool=%s | "
            "success=%s | latency=%.4f seconds | error=%s",
            trace_id,
            tool_name,
            False,
            latency,
            error,
        )

        return metadata


def main():
    print("=== Tool Result Observability ===")

    successful_call = observe_tool_call(
        tool_name="get_weather",
        arguments={"city": "Kolkata"},
    )

    failed_call = observe_tool_call(
        tool_name="get_weather",
        arguments={"city": "Unknown City"},
    )

    print("\n=== Tool Result Summary ===")

    for result in (successful_call, failed_call):
        print(f"\nTrace ID:       {result['trace_id']}")
        print(f"Tool:           {result['tool']}")
        print(f"Arguments:      {result['arguments']}")
        print(f"Success:        {result['success']}")
        print(f"Latency:        {result['latency_seconds']} seconds")
        print(f"Result:         {result['result']}")

        if not result["success"]:
            print(f"Error:          {result['error']}")


if __name__ == "__main__":
    main()
