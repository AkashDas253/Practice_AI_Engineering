from pydantic import ValidationError

from models import (
    AddTodoInput,
    SearchTodoInput,
    TodoIdInput,
    UpdateTodoInput,
)

from todo_store import (
    add_todo,
    clear_completed_todos,
    complete_todo,
    delete_todo,
    get_subtasks,
    list_todos,
    search_todos,
    update_todo,
)


def _error(message: str) -> dict:
    return {
        "success": False,
        "error": message,
    }


# Add a task or subtask.

def add_todo_tool(
    title: str,
    due_at: str | None = None,
    parent_id: int | None = None,
) -> dict:

    try:

        data = AddTodoInput(
            title=title,
            due_at=due_at,
            parent_id=parent_id,
        )

        todo = add_todo(
            title=data.title,
            due_at=data.due_at,
            parent_id=data.parent_id,
        )

        return {
            "success": True,
            "todo": todo.model_dump(),
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# List all tasks.

def list_todos_tool() -> dict:

    try:

        todos = list_todos()

        return {
            "success": True,
            "count": len(todos),
            "todos": [
                todo.model_dump()
                for todo in todos
            ],
        }

    except Exception as error:

        return _error(
            str(error)
        )


# Search tasks.

def search_todos_tool(
    query: str,
) -> dict:

    try:

        data = SearchTodoInput(
            query=query
        )

        todos = search_todos(
            data.query
        )

        return {
            "success": True,
            "count": len(todos),
            "todos": [
                todo.model_dump()
                for todo in todos
            ],
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# List subtasks.

def list_subtasks_tool(
    parent_id: int,
) -> dict:

    try:

        data = TodoIdInput(
            todo_id=parent_id
        )

        todos = get_subtasks(
            data.todo_id
        )

        return {
            "success": True,
            "parent_id": data.todo_id,
            "count": len(todos),
            "subtasks": [
                todo.model_dump()
                for todo in todos
            ],
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# Complete a task.

def complete_todo_tool(
    todo_id: int,
) -> dict:

    try:

        data = TodoIdInput(
            todo_id=todo_id
        )

        todo = complete_todo(
            data.todo_id
        )

        if todo is None:

            return _error(
                f"Todo {todo_id} not found."
            )

        return {
            "success": True,
            "todo": todo.model_dump(),
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# Update a task.

def update_todo_tool(
    todo_id: int,
    title: str | None = None,
    due_at: str | None = None,
) -> dict:

    try:

        data = UpdateTodoInput(
            todo_id=todo_id,
            title=title,
            due_at=due_at,
        )

        if (
            data.title is None
            and data.due_at is None
        ):
            return _error(
                "Provide a new title or due date/time."
            )

        todo = update_todo(
            todo_id=data.todo_id,
            title=data.title,
            due_at=data.due_at,
        )

        if todo is None:

            return _error(
                f"Todo {todo_id} not found."
            )

        return {
            "success": True,
            "todo": todo.model_dump(),
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# Delete a task.

def delete_todo_tool(
    todo_id: int,
) -> dict:

    try:

        data = TodoIdInput(
            todo_id=todo_id
        )

        deleted = delete_todo(
            data.todo_id
        )

        if not deleted:

            return _error(
                f"Todo {todo_id} not found."
            )

        return {
            "success": True,
            "message": (
                f"Todo {todo_id} "
                "and its subtasks deleted."
            ),
        }

    except ValidationError as error:

        return _error(
            str(error)
        )

    except Exception as error:

        return _error(
            str(error)
        )


# Remove completed tasks.

def clear_completed_todos_tool() -> dict:

    try:

        count = clear_completed_todos()

        return {
            "success": True,
            "deleted_count": count,
        }

    except Exception as error:

        return _error(
            str(error)
        )
