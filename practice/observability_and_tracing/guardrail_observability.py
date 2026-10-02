import logging
import uuid


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


def check_guardrail(action: str, arguments: dict) -> dict:
    """Check whether an action is allowed."""
    trace_id = str(uuid.uuid4())

    logger.info(
        "Guardrail check started | trace_id=%s | action=%s | arguments=%s",
        trace_id,
        action,
        arguments,
    )

    try:
        if action == "get_weather":
            decision = "allow"
            reason = "Action is permitted."

        elif action == "delete_file":
            decision = "block"
            reason = "File deletion is not permitted."

        elif action == "trigger_guardrail_error":
            raise RuntimeError("Guardrail service unavailable")

        else:
            decision = "block"
            reason = f"Unknown action: {action}"

        logger.info(
            "Guardrail decision | trace_id=%s | action=%s | decision=%s | reason=%s",
            trace_id,
            action,
            decision,
            reason,
        )

        return {
            "trace_id": trace_id,
            "action": action,
            "arguments": arguments,
            "decision": decision,
            "reason": reason,
            "success": True,
        }

    except Exception as error:
        logger.exception(
            "Guardrail check failed | trace_id=%s | action=%s | error=%s",
            trace_id,
            action,
            error,
        )

        return {
            "trace_id": trace_id,
            "action": action,
            "arguments": arguments,
            "decision": "error",
            "reason": str(error),
            "success": False,
        }


def execute_action(action: str, arguments: dict) -> dict:
    """Simulate execution of an allowed action."""
    if action == "get_weather":
        return {
            "city": arguments["city"],
            "temperature_c": 30,
            "condition": "Sunny",
        }

    raise ValueError(f"Action execution failed: {action}")


def run_guardrail_flow(action: str, arguments: dict) -> dict:
    """Run guardrail check and execute the action when allowed."""
    guardrail = check_guardrail(action, arguments)

    if not guardrail["success"]:
        logger.error(
            "Guardrail failure recorded | trace_id=%s | action=%s | error=%s",
            guardrail["trace_id"],
            action,
            guardrail["reason"],
        )

        guardrail["blocked"] = False
        guardrail["result"] = None

        return guardrail

    if guardrail["decision"] == "block":
        logger.warning(
            "Action blocked | trace_id=%s | action=%s | reason=%s",
            guardrail["trace_id"],
            action,
            guardrail["reason"],
        )

        guardrail["blocked"] = True
        guardrail["result"] = None

        return guardrail

    try:
        result = execute_action(action, arguments)

        logger.info(
            "Action allowed and executed | trace_id=%s | action=%s | result=%s",
            guardrail["trace_id"],
            action,
            result,
        )

        guardrail["blocked"] = False
        guardrail["result"] = result

        return guardrail

    except Exception as error:
        logger.exception(
            "Action execution failed | trace_id=%s | action=%s | error=%s",
            guardrail["trace_id"],
            action,
            error,
        )

        guardrail["blocked"] = False
        guardrail["result"] = None
        guardrail["execution_error"] = str(error)

        return guardrail


def main():
    print("=== Guardrail Observability ===")

    allowed_result = run_guardrail_flow(
        action="get_weather",
        arguments={"city": "Kolkata"},
    )

    blocked_result = run_guardrail_flow(
        action="delete_file",
        arguments={"path": "important.txt"},
    )

    failed_result = run_guardrail_flow(
        action="trigger_guardrail_error",
        arguments={},
    )

    print("\n=== Guardrail Summary ===")

    results = [
        ("Allowed action", allowed_result),
        ("Blocked action", blocked_result),
        ("Guardrail failure", failed_result),
    ]

    for name, result in results:
        print(f"\n--- {name} ---")
        print(f"Trace ID:       {result['trace_id']}")
        print(f"Action:         {result['action']}")
        print(f"Decision:       {result['decision']}")
        print(f"Success:        {result['success']}")
        print(f"Reason:         {result['reason']}")
        print(f"Blocked:        {result.get('blocked', False)}")
        print(f"Result:         {result.get('result')}")


if __name__ == "__main__":
    main()
