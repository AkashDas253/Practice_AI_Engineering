import logging
import uuid

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()

MODEL_NAME = "models/gemini-3.5-flash-lite"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def get_weather(city):
    weather_data = {
        "Kolkata": {
            "city": "Kolkata",
            "temperature_c": 30,
            "condition": "Sunny",
        },
        "Delhi": {
            "city": "Delhi",
            "temperature_c": 32,
            "condition": "Clear",
        },
    }

    if city not in weather_data:
        raise ValueError(f"Weather data not available for {city}")

    return weather_data[city]


weather_function = types.FunctionDeclaration(
    name="get_weather",
    description="Get the current weather for a city.",
    parameters=types.Schema(
        type="OBJECT",
        properties={
            "city": types.Schema(
                type="STRING",
                description="Name of the city.",
            )
        },
        required=["city"],
    ),
)


weather_tool_config = types.Tool(
    function_declarations=[weather_function]
)


def run_agent(task):
    client = genai.Client()

    trace_id = str(uuid.uuid4())

    logging.info(
        "Agent started | trace_id=%s | task=%s",
        trace_id,
        task,
    )

    contents = [
        types.Content(
            role="user",
            parts=[
                types.Part.from_text(text=task)
            ],
        )
    ]

    config = types.GenerateContentConfig(
        tools=[weather_tool_config],
        system_instruction=(
            "You are a helpful assistant. "
            "When the user asks for weather information, "
            "use the get_weather tool."
        ),
    )

    step = 1

    logging.info(
        "Agent step | trace_id=%s | step=%s | action=model_request",
        trace_id,
        step,
    )

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )

    function_call = None

    for part in response.candidates[0].content.parts:
        if part.function_call:
            function_call = part.function_call
            break

    if function_call is None:
        final_answer = response.text.strip()

        step += 1

        logging.info(
            "Agent final response | trace_id=%s | step=%s | answer=%s",
            trace_id,
            step,
            final_answer,
        )

        logging.info(
            "Agent completed | trace_id=%s | steps=%s",
            trace_id,
            step,
        )

        return {
            "trace_id": trace_id,
            "answer": final_answer,
        }

    step += 1

    logging.info(
        "Agent decision | trace_id=%s | step=%s | tool=%s | arguments=%s",
        trace_id,
        step,
        function_call.name,
        function_call.args,
    )

    tool_result = get_weather(**function_call.args)

    step += 1

    logging.info(
        "Tool observation | trace_id=%s | step=%s | result=%s",
        trace_id,
        step,
        tool_result,
    )

    # Preserve the model's function-call response.
    contents.append(response.candidates[0].content)

    # Create the function response.
    function_response = types.Part.from_function_response(
        name=function_call.name,
        response=tool_result,
    )

    # Gemini expects the function response inside a user content
    # message rather than a content with role="tool".
    contents.append(
        types.Content(
            role="user",
            parts=[function_response],
        )
    )

    step += 1

    logging.info(
        "Agent step | trace_id=%s | step=%s | action=model_final_response",
        trace_id,
        step,
    )

    final_response = client.models.generate_content(
        model=MODEL_NAME,
        contents=contents,
        config=config,
    )

    final_answer = final_response.text.strip()

    step += 1

    logging.info(
        "Agent final response | trace_id=%s | step=%s | answer=%s",
        trace_id,
        step,
        final_answer,
    )

    logging.info(
        "Agent completed | trace_id=%s | steps=%s",
        trace_id,
        step,
    )

    return {
        "trace_id": trace_id,
        "answer": final_answer,
    }


if __name__ == "__main__":
    task = "Find the current weather in Kolkata."

    print("=== Agent Execution Trace ===")
    print(f"Model: {MODEL_NAME}")
    print(f"Task: {task}")

    trace = run_agent(task)

    print()
    print("=== Final Result ===")
    print(f"Trace ID: {trace['trace_id']}")
    print(f"Answer: {trace['answer']}")
