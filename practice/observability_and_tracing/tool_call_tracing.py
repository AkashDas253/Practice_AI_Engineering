import logging
import uuid


# Logging setup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Tool

def get_weather(city: str) -> dict:
    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        },
        "Paris": {
            "city": "Paris",
            "temperature_c": 18,
            "condition": "Cloudy",
        },
    }

    if city not in weather_data:
        raise ValueError(f"Weather data not available for {city}")

    return weather_data[city]


# Trace a tool call

def trace_tool_call(tool_name: str, arguments: dict):
    trace_id = str(uuid.uuid4())

    logger.info(
        "Tool request | trace_id=%s | tool=%s | arguments=%s",
        trace_id,
        tool_name,
        arguments,
    )

    try:
        if tool_name == "get_weather":
            result = get_weather(**arguments)
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        logger.info(
            "Tool result | trace_id=%s | tool=%s | result=%s",
            trace_id,
            tool_name,
            result,
        )

        return result

    except Exception as error:
        logger.error(
            "Tool error | trace_id=%s | tool=%s | error=%s",
            trace_id,
            tool_name,
            error,
        )

        return None


# Successful tool call

trace_tool_call(
    "get_weather",
    {"city": "Kolkata"},
)


# Tool call that produces an error

trace_tool_call(
    "get_weather",
    {"city": "Unknown City"},
)
