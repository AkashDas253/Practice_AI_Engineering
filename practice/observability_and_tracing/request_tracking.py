import logging
import uuid


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Create a request ID

request_id = str(uuid.uuid4())


# Application event

logger.info(
    "Request started | request_id=%s",
    request_id,
)


# Model event

logger.info(
    "Model request started | request_id=%s | model=%s",
    request_id,
    "models/gemini-3.5-flash-lite",
)

logger.info(
    "Model request completed | request_id=%s",
    request_id,
)


# Tool event

logger.info(
    "Tool call started | request_id=%s | tool=%s",
    request_id,
    "get_weather",
)

logger.info(
    "Tool call completed | request_id=%s | tool=%s | city=%s",
    request_id,
    "get_weather",
    "Kolkata",
)


# Agent event

logger.info(
    "Agent step completed | request_id=%s | step=%s",
    request_id,
    1,
)

logger.info(
    "Agent completed | request_id=%s",
    request_id,
)


# Application event

logger.info(
    "Request finished | request_id=%s",
    request_id,
)
