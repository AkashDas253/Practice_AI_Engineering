import logging
import uuid


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Agent steps

def run_agent(task: str):
    trace_id = str(uuid.uuid4())

    logger.info(
        "Agent started | trace_id=%s | task=%s",
        trace_id,
        task,
    )

    # Step 1: Understand the task

    logger.info(
        "Agent step | trace_id=%s | step=1 | action=understand_task",
        trace_id,
    )

    # Step 2: Decide what tool is needed

    logger.info(
        "Agent step | trace_id=%s | step=2 | action=select_tool | tool=get_weather",
        trace_id,
    )

    # Step 3: Execute the tool

    logger.info(
        "Agent step | trace_id=%s | step=3 | action=execute_tool | tool=get_weather",
        trace_id,
    )

    tool_result = {
        "city": "Kolkata",
        "temperature_c": 30,
        "condition": "Sunny",
    }

    logger.info(
        "Agent observation | trace_id=%s | step=3 | result=%s",
        trace_id,
        tool_result,
    )

    # Step 4: Produce the final answer

    logger.info(
        "Agent step | trace_id=%s | step=4 | action=produce_answer",
        trace_id,
    )

    answer = (
        "The current temperature in Kolkata is 30°C "
        "and the weather is Sunny."
    )

    logger.info(
        "Agent completed | trace_id=%s | answer=%s",
        trace_id,
        answer,
    )


# Run the agent

run_agent(
    "Find the current weather in Kolkata."
)
