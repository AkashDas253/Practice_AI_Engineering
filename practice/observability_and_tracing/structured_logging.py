import json
import logging


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

logger = logging.getLogger(__name__)


# Structured logging helper

def log_event(event: str, **data):
    log_entry = {
        "event": event,
        **data,
    }

    logger.info(json.dumps(log_entry))


# Application event

log_event(
    "application_started",
)


# Model event

log_event(
    "model_request_started",
    model="models/gemini-3.5-flash-lite",
    prompt="What is Python?",
)

log_event(
    "model_request_completed",
    model="models/gemini-3.5-flash-lite",
    response="Python is a programming language.",
)


# Tool event

log_event(
    "tool_call_started",
    tool="get_weather",
    arguments={
        "city": "Kolkata",
    },
)

log_event(
    "tool_call_completed",
    tool="get_weather",
    result={
        "city": "Kolkata",
        "temperature_c": 30,
        "condition": "Sunny",
    },
)


# Agent event

log_event(
    "agent_step_completed",
    step=1,
)

log_event(
    "agent_completed",
)


# Application event

log_event(
    "application_finished",
)
