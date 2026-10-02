import logging
import uuid


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Trace context

class TraceContext:
    def __init__(self):
        self.trace_id = str(uuid.uuid4())


# Model call

def call_model(context: TraceContext, prompt: str) -> str:
    logger.info(
        "Model call | trace_id=%s | prompt=%s",
        context.trace_id,
        prompt,
    )

    return "get_weather"


# Tool call

def call_tool(
    context: TraceContext,
    tool_name: str,
    arguments: dict,
) -> dict:

    logger.info(
        "Tool call | trace_id=%s | tool=%s | arguments=%s",
        context.trace_id,
        tool_name,
        arguments,
    )

    result = {
        "city": "Kolkata",
        "temperature_c": 30,
        "condition": "Sunny",
    }

    logger.info(
        "Tool result | trace_id=%s | result=%s",
        context.trace_id,
        result,
    )

    return result


# Agent execution

def run_agent(task: str):

    context = TraceContext()

    logger.info(
        "Agent started | trace_id=%s | task=%s",
        context.trace_id,
        task,
    )

    # Agent step

    logger.info(
        "Agent step | trace_id=%s | step=1 | action=understand_task",
        context.trace_id,
    )

    # Model call

    tool_name = call_model(
        context,
        "Determine which tool is needed.",
    )

    # Agent step

    logger.info(
        "Agent step | trace_id=%s | step=2 | action=tool_selected | tool=%s",
        context.trace_id,
        tool_name,
    )

    # Tool call

    result = call_tool(
        context,
        tool_name,
        {"city": "Kolkata"},
    )

    # Final agent step

    logger.info(
        "Agent step | trace_id=%s | step=3 | action=produce_answer",
        context.trace_id,
    )

    answer = (
        f"The current temperature in {result['city']} "
        f"is {result['temperature_c']}°C."
    )

    logger.info(
        "Agent completed | trace_id=%s | answer=%s",
        context.trace_id,
        answer,
    )


# Run the agent

run_agent(
    "Find the current temperature in Kolkata."
)
