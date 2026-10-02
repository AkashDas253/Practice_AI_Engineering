import logging
import time
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_agent(task: str) -> None:
    trace_id = str(uuid.uuid4())

    logging.info(
        "Trace started | trace_id=%s | task=%s",
        trace_id,
        task,
    )

    # Parent span: agent operation
    agent_span_id = str(uuid.uuid4())

    logging.info(
        "Agent span started | trace_id=%s | span_id=%s",
        trace_id,
        agent_span_id,
    )

    # Child span: model operation
    model_span_id = str(uuid.uuid4())

    logging.info(
        "Model span started | trace_id=%s | span_id=%s | parent_span_id=%s",
        trace_id,
        model_span_id,
        agent_span_id,
    )

    time.sleep(0.05)

    logging.info(
        "Model span completed | trace_id=%s | span_id=%s | parent_span_id=%s",
        trace_id,
        model_span_id,
        agent_span_id,
    )

    # Child span: tool operation
    tool_span_id = str(uuid.uuid4())

    logging.info(
        "Tool span started | trace_id=%s | span_id=%s | parent_span_id=%s | tool=get_weather",
        trace_id,
        tool_span_id,
        agent_span_id,
    )

    time.sleep(0.05)

    result = {
        "city": "Kolkata",
        "temperature_c": 30,
        "condition": "Sunny",
    }

    logging.info(
        "Tool span completed | trace_id=%s | span_id=%s | parent_span_id=%s | result=%s",
        trace_id,
        tool_span_id,
        agent_span_id,
        result,
    )

    logging.info(
        "Agent span completed | trace_id=%s | span_id=%s",
        trace_id,
        agent_span_id,
    )

    logging.info(
        "Trace completed | trace_id=%s",
        trace_id,
    )


task = "Find the current weather in Kolkata."

print("=== Nested Spans ===")
print(f"Task: {task}")

run_agent(task)
