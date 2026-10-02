import logging
import os
import time
import uuid
from pathlib import Path

from dotenv import load_dotenv
from google import genai


MODEL = "models/gemini-3.5-flash-lite"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)


# Load .env from the same folder as this script.
ENV_FILE = Path(__file__).resolve().parent / ".env"
load_dotenv(ENV_FILE)


def get_weather(city: str) -> dict:
    if city.lower() == "kolkata":
        return {
            "city": city,
            "temperature_c": 30,
            "condition": "Sunny",
        }

    raise ValueError(f"Weather data not available for {city}")


def check_guardrail(action: str, arguments: dict) -> tuple[str, str]:
    if action == "get_weather":
        return "allow", "Action is permitted."

    return "block", f"Action is not permitted: {action}"


def model_call(client, prompt: str, trace_id: str, step: int):
    start = time.perf_counter()

    logger.info(
        "Model request started | trace_id=%s | step=%s | prompt=%s",
        trace_id,
        step,
        prompt,
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=prompt,
    )

    latency = time.perf_counter() - start

    logger.info(
        "Model request completed | trace_id=%s | step=%s | latency=%.4f seconds",
        trace_id,
        step,
        latency,
    )

    return response.text, latency


def run_agent(task: str):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        raise RuntimeError(
            f"GEMINI_API_KEY not found in {ENV_FILE}"
        )

    client = genai.Client(api_key=api_key)

    trace_id = str(uuid.uuid4())
    trace = []

    logger.info(
        "Application started | trace_id=%s | task=%s",
        trace_id,
        task,
    )

    trace.append({
        "step": 1,
        "type": "user_request",
        "task": task,
    })

    # Model decides which tool is needed.
    decision_prompt = (
        "You are an agent.\n"
        f"User task: {task}\n\n"
        "Determine the tool needed.\n"
        "Return only the tool name and city.\n"
        "Use this format:\n"
        "tool=get_weather\n"
        "city=Kolkata"
    )

    decision, model_latency_1 = model_call(
        client,
        decision_prompt,
        trace_id,
        2,
    )

    logger.info(
        "Agent decision | trace_id=%s | step=2 | decision=%s",
        trace_id,
        decision.replace("\n", " | "),
    )

    trace.append({
        "step": 2,
        "type": "model_decision",
        "decision": decision,
        "latency": model_latency_1,
    })

    # Use the city from this example task.
    city = "Kolkata"
    tool_name = "get_weather"
    arguments = {"city": city}

    # Check the tool with the guardrail.
    guardrail_start = time.perf_counter()

    logger.info(
        "Guardrail check started | trace_id=%s | step=3 | action=%s | arguments=%s",
        trace_id,
        tool_name,
        arguments,
    )

    guardrail_decision, reason = check_guardrail(
        tool_name,
        arguments,
    )

    guardrail_latency = time.perf_counter() - guardrail_start

    logger.info(
        "Guardrail decision | trace_id=%s | step=3 | decision=%s | reason=%s | latency=%.4f seconds",
        trace_id,
        guardrail_decision,
        reason,
        guardrail_latency,
    )

    trace.append({
        "step": 3,
        "type": "guardrail",
        "decision": guardrail_decision,
        "reason": reason,
        "latency": guardrail_latency,
    })

    if guardrail_decision != "allow":
        logger.warning(
            "Action blocked | trace_id=%s | action=%s | reason=%s",
            trace_id,
            tool_name,
            reason,
        )

        return {
            "trace_id": trace_id,
            "answer": "The requested action was blocked.",
            "trace": trace,
        }

    # Execute the tool.
    tool_start = time.perf_counter()

    logger.info(
        "Tool call started | trace_id=%s | step=4 | tool=%s | arguments=%s",
        trace_id,
        tool_name,
        arguments,
    )

    try:
        tool_result = get_weather(city)
        tool_error = None
    except Exception as exc:
        tool_result = None
        tool_error = str(exc)

    tool_latency = time.perf_counter() - tool_start

    if tool_error:
        logger.error(
            "Tool call failed | trace_id=%s | step=4 | tool=%s | error=%s | latency=%.4f seconds",
            trace_id,
            tool_name,
            tool_error,
            tool_latency,
        )

        trace.append({
            "step": 4,
            "type": "tool",
            "tool": tool_name,
            "success": False,
            "error": tool_error,
            "latency": tool_latency,
        })

        return {
            "trace_id": trace_id,
            "answer": "The tool call failed.",
            "trace": trace,
        }

    logger.info(
        "Tool call completed | trace_id=%s | step=4 | tool=%s | result=%s | latency=%.4f seconds",
        trace_id,
        tool_name,
        tool_result,
        tool_latency,
    )

    trace.append({
        "step": 4,
        "type": "tool",
        "tool": tool_name,
        "success": True,
        "result": tool_result,
        "latency": tool_latency,
    })

    # Model produces the final answer.
    final_prompt = (
        "Answer the user's question using the tool result.\n\n"
        f"User task: {task}\n"
        f"Tool result: {tool_result}\n\n"
        "Give a concise answer."
    )

    final_answer, model_latency_2 = model_call(
        client,
        final_prompt,
        trace_id,
        5,
    )

    logger.info(
        "Final response | trace_id=%s | step=5 | answer=%s",
        trace_id,
        final_answer,
    )

    trace.append({
        "step": 5,
        "type": "final_response",
        "answer": final_answer,
        "latency": model_latency_2,
    })

    total_latency = (
        model_latency_1
        + guardrail_latency
        + tool_latency
        + model_latency_2
    )

    logger.info(
        "Application completed | trace_id=%s | steps=%s | total_latency=%.4f seconds",
        trace_id,
        len(trace),
        total_latency,
    )

    return {
        "trace_id": trace_id,
        "answer": final_answer,
        "trace": trace,
        "total_latency": total_latency,
    }


if __name__ == "__main__":
    print("=== End-to-End Observability ===")
    print(f"Model: {MODEL}")

    task = "Find the current weather in Kolkata."

    result = run_agent(task)

    print("\n=== Final Result ===")
    print(f"Trace ID: {result['trace_id']}")
    print(f"Answer: {result['answer']}")
    print(f"Steps: {len(result['trace'])}")
    print(f"Total latency: {result['total_latency']:.4f} seconds")
