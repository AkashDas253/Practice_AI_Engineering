import logging
import os
import uuid

from dotenv import load_dotenv
from google import genai


load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

logger = logging.getLogger(__name__)

MODEL = "models/gemini-3.5-flash-lite"


def run_agent(task: str):
    client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

    trace_id = str(uuid.uuid4())

    context = [
        f"User task: {task}",
    ]

    logger.info(
        "Agent started | trace_id=%s | task=%s",
        trace_id,
        task,
    )

    # Step 1: Understand the task
    step = 1

    logger.info(
        "Agent step | trace_id=%s | step=%s | action=understand_task | context_items=%s",
        trace_id,
        step,
        len(context),
    )

    context.append(
        "The user wants the current weather for Kolkata."
    )

    logger.info(
        "Context updated | trace_id=%s | step=%s | context_items=%s",
        trace_id,
        step,
        len(context),
    )

    # Step 2: Ask the model to select the tool
    step = 2

    model_prompt = f"""
You are an AI agent.

Task:
{task}

Available tool:
get_weather(city)

Determine which city should be passed to the tool.
Return only the city name.
"""

    logger.info(
        "Model request | trace_id=%s | step=%s | context_items=%s | context_chars=%s",
        trace_id,
        step,
        len(context),
        sum(len(item) for item in context),
    )

    response = client.models.generate_content(
        model=MODEL,
        contents=model_prompt,
    )

    city = "Kolkata"

    logger.info(
        "Model response | trace_id=%s | step=%s | response=%s",
        trace_id,
        step,
        response.text.strip(),
    )

    context.append(
        f"Selected tool: get_weather(city='{city}')"
    )

    logger.info(
        "Context updated | trace_id=%s | step=%s | context_items=%s",
        trace_id,
        step,
        len(context),
    )

    # Step 3: Execute the tool
    step = 3

    weather_result = {
        "city": city,
        "temperature_c": 30,
        "condition": "Sunny",
    }

    logger.info(
        "Tool result | trace_id=%s | step=%s | result=%s",
        trace_id,
        step,
        weather_result,
    )

    context.append(
        f"Tool result: {weather_result}"
    )

    logger.info(
        "Context updated | trace_id=%s | step=%s | context_items=%s",
        trace_id,
        step,
        len(context),
    )

    # Step 4: Produce the final answer using accumulated context
    step = 4

    final_prompt = f"""
You are completing an agent task.

Original task:
{task}

Context accumulated during the agent execution:
{chr(10).join(context)}

Using the context above, provide a concise final answer.
"""

    logger.info(
        "Model request | trace_id=%s | step=%s | context_items=%s | context_chars=%s",
        trace_id,
        step,
        len(context),
        sum(len(item) for item in context),
    )

    final_response = client.models.generate_content(
        model=MODEL,
        contents=final_prompt,
    )

    answer = final_response.text.strip()

    logger.info(
        "Agent completed | trace_id=%s | step=%s | final_context_items=%s | final_context_chars=%s",
        trace_id,
        step,
        len(context),
        sum(len(item) for item in context),
    )

    return {
        "trace_id": trace_id,
        "context": context,
        "answer": answer,
    }


def main():
    print("=== Context Usage Tracking ===")
    print(f"Model: {MODEL}")

    task = "Find the current weather in Kolkata."

    result = run_agent(task)

    print("\n=== Final Result ===")
    print(f"Trace ID: {result['trace_id']}")
    print(f"Context items: {len(result['context'])}")
    print(
        f"Context characters: "
        f"{sum(len(item) for item in result['context'])}"
    )
    print(f"Answer: {result['answer']}")

    print("\n=== Context Supplied to Agent ===")

    for index, item in enumerate(result["context"], start=1):
        print(f"{index}. {item}")


if __name__ == "__main__":
    main()
