import json
from datetime import datetime, timezone
from pathlib import Path

from models import Todo


# Application data is stored separately from source code.

BASE_DIR = Path(__file__).resolve().parent

OUTPUT_DIR = BASE_DIR / "output"

TODO_FILE = OUTPUT_DIR / "todos.json"


# Time helper.

def utc_now() -> str:
    return datetime.now(
        timezone.utc
    ).isoformat()


# Storage helpers.

def _load() -> list[Todo]:

    if not TODO_FILE.exists():
        return []

    try:
        data = json.loads(
            TODO_FILE.read_text(
                encoding="utf-8"
            )
        )

    except (
        json.JSONDecodeError,
        OSError,
    ):
        return []

    return [
        Todo.model_validate(todo)
        for todo in data
    ]


def _save(todos: list[Todo]) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    TODO_FILE.write_text(
        json.dumps(
            [
                todo.model_dump()
                for todo in todos
            ],
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


# Create.

def add_todo(
    title: str,
    due_at: str | None = None,
    parent_id: int | None = None,
) -> Todo:

    todos = _load()

    if parent_id is not None:

        parent_exists = any(
            todo.id == parent_id
            for todo in todos
        )

        if not parent_exists:
            raise ValueError(
                f"Parent todo {parent_id} not found."
            )

    next_id = max(
        (
            todo.id
            for todo in todos
        ),
        default=0,
    ) + 1

    todo = Todo(
        id=next_id,
        title=title.strip(),
        due_at=due_at,
        parent_id=parent_id,
        created_at=utc_now(),
    )

    todos.append(todo)

    _save(todos)

    return todo


# Read.

def list_todos() -> list[Todo]:
    return _load()


def get_todo(
    todo_id: int,
) -> Todo | None:

    for todo in _load():

        if todo.id == todo_id:
            return todo

    return None


def search_todos(
    query: str,
) -> list[Todo]:

    query = query.strip().lower()

    return [
        todo
        for todo in _load()
        if query in todo.title.lower()
    ]


def get_subtasks(
    parent_id: int,
) -> list[Todo]:

    return [
        todo
        for todo in _load()
        if todo.parent_id == parent_id
    ]


# Update.

def update_todo(
    todo_id: int,
    title: str | None = None,
    due_at: str | None = None,
) -> Todo | None:

    todos = _load()

    for todo in todos:

        if todo.id != todo_id:
            continue

        if title is not None:
            todo.title = title.strip()

        if due_at is not None:
            todo.due_at = due_at

            # A changed due time creates a new reminder.
            todo.reminder_sent = False

        todo.updated_at = utc_now()

        _save(todos)

        return todo

    return None


# Complete.

def complete_todo(
    todo_id: int,
) -> Todo | None:

    todos = _load()

    for todo in todos:

        if todo.id != todo_id:
            continue

        if todo.completed:
            return todo

        todo.completed = True
        todo.completed_at = utc_now()
        todo.updated_at = utc_now()

        _save(todos)

        return todo

    return None


# Delete.

def delete_todo(
    todo_id: int,
) -> bool:

    todos = _load()

    ids_to_delete = {
        todo_id
    }

    changed = True

    # Parent deletion includes all descendant tasks.
    while changed:

        changed = False

        for todo in todos:

            if (
                todo.parent_id in ids_to_delete
                and todo.id not in ids_to_delete
            ):
                ids_to_delete.add(todo.id)
                changed = True

    updated_todos = [
        todo
        for todo in todos
        if todo.id not in ids_to_delete
    ]

    if len(updated_todos) == len(todos):
        return False

    _save(updated_todos)

    return True


# Cleanup.

def clear_completed_todos() -> int:

    todos = _load()

    completed_ids = {
        todo.id
        for todo in todos
        if todo.completed
    }

    changed = True

    while changed:

        changed = False

        for todo in todos:

            if (
                todo.parent_id in completed_ids
                and todo.id not in completed_ids
            ):
                completed_ids.add(todo.id)
                changed = True

    remaining = [
        todo
        for todo in todos
        if todo.id not in completed_ids
    ]

    deleted_count = (
        len(todos)
        - len(remaining)
    )

    if deleted_count:
        _save(remaining)

    return deleted_count


# Reminder support.

def get_due_todos() -> list[Todo]:

    now = datetime.now(
        timezone.utc
    )

    due_todos = []

    for todo in _load():

        if todo.completed:
            continue

        if todo.reminder_sent:
            continue

        if not todo.due_at:
            continue

        try:
            due_at = datetime.fromisoformat(
                todo.due_at
            )

        except ValueError:
            continue

        if due_at.tzinfo is None:
            due_at = due_at.replace(
                tzinfo=timezone.utc
            )

        if due_at.astimezone(
            timezone.utc
        ) <= now:

            due_todos.append(todo)

    return due_todos


def mark_reminder_sent(
    todo_id: int,
) -> None:

    todos = _load()

    for todo in todos:

        if todo.id != todo_id:
            continue

        todo.reminder_sent = True
        todo.updated_at = utc_now()

        _save(todos)

        return
