import logging


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Application event

logger.info("Application started")


# Model event

logger.info("Model request started")

model = "models/gemini-3.5-flash-lite"
prompt = "What is Python?"

logger.info(
    "Model request completed | model=%s | prompt=%s",
    model,
    prompt,
)


# Tool event

logger.info("Tool call started | tool=get_weather")

tool_result = {
    "city": "Kolkata",
    "temperature_c": 30,
    "condition": "Sunny",
}

logger.info(
    "Tool call completed | tool=get_weather | result=%s",
    tool_result,
)


# Agent event

logger.info("Agent step completed | step=1")
logger.info("Agent completed")


# Application event

logger.info("Application finished")
