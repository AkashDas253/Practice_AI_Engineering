import logging
import uuid

from dotenv import load_dotenv
from google import genai


load_dotenv()

MODEL_NAME = "models/gemini-3.5-flash-lite"


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)


def run_conversation():
    client = genai.Client()

    conversation_id = str(uuid.uuid4())

    logging.info(
        "Conversation started | conversation_id=%s",
        conversation_id,
    )

    chat = client.chats.create(
        model=MODEL_NAME,
    )

    turns = [
        "What is Python? Answer in one sentence.",
        "What is it commonly used for? Answer in one sentence.",
        "Name one advantage of using it. Answer in one sentence.",
    ]

    responses = []

    for turn_number, prompt in enumerate(turns, start=1):
        logging.info(
            "Conversation turn started | conversation_id=%s | turn=%s | prompt=%s",
            conversation_id,
            turn_number,
            prompt,
        )

        response = chat.send_message(prompt)

        answer = response.text.strip()

        responses.append(
            {
                "turn": turn_number,
                "prompt": prompt,
                "answer": answer,
            }
        )

        logging.info(
            "Conversation turn completed | conversation_id=%s | turn=%s | answer=%s",
            conversation_id,
            turn_number,
            answer,
        )

    logging.info(
        "Conversation completed | conversation_id=%s | turns=%s",
        conversation_id,
        len(responses),
    )

    return conversation_id, responses


if __name__ == "__main__":
    print("=== Conversation Tracing ===")
    print(f"Model: {MODEL_NAME}")

    conversation_id, responses = run_conversation()

    print()
    print("=== Conversation ===")
    print(f"Conversation ID: {conversation_id}")

    for item in responses:
        print()
        print(f"--- Turn {item['turn']} ---")
        print(f"Prompt: {item['prompt']}")
        print(f"Response: {item['answer']}")
