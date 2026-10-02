import logging
import uuid


# Configuration

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


# Example operations

def model_call() -> str:
    """Simulates a model operation that fails."""

    raise RuntimeError("Model request failed")


def tool_call(city: str) -> dict:
    """Simulates a tool operation."""

    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        }
    }

    if city not in weather_data:
        raise ValueError(
            f"Weather data not available for {city}"
        )

    return weather_data[city]


def application_operation() -> None:
    """Simulates an application-level failure."""

    raise RuntimeError("Application configuration error")


# Track errors

print("=== Error Tracking ===")

errors = {
    "model": None,
    "tool": None,
    "application": None,
}


# Model error

model_trace_id = str(uuid.uuid4())

logging.info(
    "Model request started | trace_id=%s",
    model_trace_id,
)

try:
    model_call()

except Exception as error:
    errors["model"] = str(error)

    logging.error(
        "Model error | trace_id=%s | error=%s",
        model_trace_id,
        error,
    )


# Tool error

tool_trace_id = str(uuid.uuid4())

logging.info(
    "Tool call started | trace_id=%s | tool=get_weather",
    tool_trace_id,
)

try:
    result = tool_call("Unknown City")

    logging.info(
        "Tool call completed | trace_id=%s | result=%s",
        tool_trace_id,
        result,
    )

except Exception as error:
    errors["tool"] = str(error)

    logging.error(
        "Tool error | trace_id=%s | tool=get_weather | error=%s",
        tool_trace_id,
        error,
    )


# Application error

application_trace_id = str(uuid.uuid4())

logging.info(
    "Application operation started | trace_id=%s",
    application_trace_id,
)

try:
    application_operation()

except Exception as error:
    errors["application"] = str(error)

    logging.error(
        "Application error | trace_id=%s | error=%s",
        application_trace_id,
        error,
    )


# Summary

total_operations = len(errors)

recorded_errors = sum(
    error is not None
    for error in errors.values()
)

successful_operations = (
    total_operations - recorded_errors
)

print("\n=== Error Tracking Summary ===")
print(f"Total operations:     {total_operations}")
print(f"Errors recorded:      {recorded_errors}")
print(f"Successful operations: {successful_operations}")
