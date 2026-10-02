import logging
import re

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def redact_string(value):
    # Redact email addresses.
    value = re.sub(
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b",
        "[REDACTED_EMAIL]",
        value,
    )

    # Redact API keys and tokens.
    value = re.sub(
        r"\b(?:sk-|AIza)[A-Za-z0-9_-]+\b",
        "[REDACTED_TOKEN]",
        value,
    )

    return value


def redact_sensitive_data(data):
    # Redact sensitive dictionary fields.
    if isinstance(data, dict):
        result = {}

        for key, value in data.items():
            if key.lower() in {
                "password",
                "api_key",
                "token",
                "access_token",
                "secret",
            }:
                result[key] = "[REDACTED]"
            elif isinstance(value, str):
                result[key] = redact_string(value)
            else:
                result[key] = redact_sensitive_data(value)

        return result

    if isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]

    return data


def process_request(request):
    # Always redact data before logging it.
    safe_request = redact_sensitive_data(request)

    logger.info("Request received | data=%s", safe_request)

    result = {
        "status": "success",
        "user_id": request["user_id"],
    }

    safe_result = redact_sensitive_data(result)

    logger.info("Request completed | result=%s", safe_result)

    return safe_result


if __name__ == "__main__":
    print("=== Sensitive Data Logging ===")

    request = {
        "user_id": "user-123",
        "email": "user@example.com",
        "password": "my-secret-password",
        "api_key": "sk-example123456789",
        "profile": {
            "name": "Alex",
            "token": "secret-token-123",
        },
    }

    print("\nOriginal data:")
    print(request)

    result = process_request(request)

    print("\nSafe result:")
    print(result)
