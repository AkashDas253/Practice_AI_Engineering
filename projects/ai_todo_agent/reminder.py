import threading
import time
from datetime import datetime

from config import REMINDER_CHECK_INTERVAL
from todo_store import (
    get_due_todos,
    mark_reminder_sent,
)


def format_due_time(
    due_at: str,
) -> str:

    try:

        due = datetime.fromisoformat(
            due_at
        )

        return due.astimezone().strftime(
            "%Y-%m-%d %I:%M %p"
        )

    except ValueError:

        return due_at


def check_reminders() -> None:

    due_todos = get_due_todos()

    for todo in due_todos:

        print(
            "\n"
            "🔔 REMINDER\n"
            f"Task: {todo.title}\n"
            f"Due: {format_due_time(todo.due_at or '')}\n"
        )

        mark_reminder_sent(
            todo.id
        )


def reminder_loop(
    stop_event: threading.Event,
) -> None:

    while not stop_event.is_set():

        try:
            check_reminders()

        except Exception as error:

            print(
                f"\nReminder error: {error}\n"
            )

        stop_event.wait(
            REMINDER_CHECK_INTERVAL
        )


def start_reminder_thread() -> tuple[
    threading.Thread,
    threading.Event,
]:

    stop_event = threading.Event()

    thread = threading.Thread(
        target=reminder_loop,
        args=(stop_event,),
        daemon=True,
        name="todo-reminder",
    )

    thread.start()

    return thread, stop_event
