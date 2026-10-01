import json
from pathlib import Path

from config import MAX_RUN_HISTORY


BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"

HISTORY_FILE = (
    OUTPUT_DIR / "history.jsonl"
)


def _read_history() -> list[dict]:

    if not HISTORY_FILE.exists():
        return []

    records = []

    with HISTORY_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:

        for line in file:

            line = line.strip()

            if not line:
                continue

            try:

                records.append(
                    json.loads(line)
                )

            except json.JSONDecodeError:
                continue

    return records


def save_run(
    user_message: str,
    response: str,
    steps: int,
    trace: list[dict],
) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    record = {
        "user_message": user_message,
        "response": response,
        "steps": steps,
        "trace": trace,
    }

    history = _read_history()

    history.append(record)

    # Keep the most recent runs only.
    history = history[
        -MAX_RUN_HISTORY:
    ]

    with HISTORY_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:

        for item in history:

            file.write(
                json.dumps(
                    item,
                    ensure_ascii=False,
                    separators=(
                        ",",
                        ":",
                    ),
                )
            )

            file.write("\n")
