import json
import logging
import uuid
from pathlib import Path
from datetime import datetime, timezone

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def create_trace():
    trace_id = str(uuid.uuid4())

    events = [
        {
            "event": "agent_started",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": 1,
        },
        {
            "event": "model_request",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": 2,
            "model": "models/gemini-3.5-flash-lite",
            "prompt": "What is Python?",
        },
        {
            "event": "tool_call",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": 3,
            "tool": "get_weather",
            "arguments": {"city": "Kolkata"},
        },
        {
            "event": "tool_result",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": 4,
            "result": {
                "city": "Kolkata",
                "temperature_c": 30,
                "condition": "Sunny",
            },
        },
        {
            "event": "agent_completed",
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "step": 5,
        },
    ]

    return {
        "trace_id": trace_id,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "events": events,
    }


def export_trace(trace, output_path):
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as file:
        json.dump(trace, file, indent=2)

    logger.info(
        "Trace exported | trace_id=%s | file=%s",
        trace["trace_id"],
        output_path,
    )


if __name__ == "__main__":
    print("=== Trace Export ===")

    trace = create_trace()

    output_path = Path("output") / "trace.json"

    export_trace(trace, output_path)

    print("\n=== Export Summary ===")
    print(f"Trace ID:      {trace['trace_id']}")
    print(f"Events:        {len(trace['events'])}")
    print(f"Output file:   {output_path}")
