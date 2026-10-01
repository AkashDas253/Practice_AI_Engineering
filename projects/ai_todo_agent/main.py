from threading import Event

from agent import run_agent
from output_store import save_run
from reminder import start_reminder_thread


def main() -> None:

    print(
        "\n=== AI TODO AGENT ==="
    )

    print(
        "Timed reminders work while this program is running."
    )

    print(
        "Type 'exit' to quit.\n"
    )

    conversation = []

    reminder_thread, stop_event = (
        start_reminder_thread()
    )

    try:

        while True:

            try:

                user_input = input(
                    "You: "
                ).strip()

            except (
                KeyboardInterrupt,
                EOFError,
            ):

                print(
                    "\nGoodbye!"
                )

                break

            if not user_input:
                continue

            if user_input.lower() in {
                "exit",
                "quit",
            }:

                print(
                    "Goodbye!"
                )

                break

            try:

                (
                    response,
                    conversation,
                    metadata,
                ) = run_agent(
                    user_message=user_input,
                    history=conversation,
                )

                save_run(
                    user_message=user_input,
                    response=response,
                    steps=metadata["steps"],
                    trace=metadata["trace"],
                )

                print(
                    f"\nAgent: {response}\n"
                )

            except Exception as error:

                print(
                    f"\nError: {error}\n"
                )

    finally:

        stop_event.set()

        reminder_thread.join(
            timeout=1
        )


if __name__ == "__main__":
    main()
