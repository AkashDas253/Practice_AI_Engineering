from pydantic import BaseModel, Field


class Todo(BaseModel):
    id: int
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    completed: bool = False

    # None means this is a top-level task.
    # A value means this task belongs to that parent task.
    parent_id: int | None = None

    created_at: str
    updated_at: str | None = None
    completed_at: str | None = None

    # ISO 8601 datetime.
    # Example: 2026-10-02T18:00:00+05:30
    due_at: str | None = None

    # Prevents repeated reminders for the same due time.
    reminder_sent: bool = False


class AddTodoInput(BaseModel):
    title: str = Field(
        min_length=1,
        max_length=200,
    )

    due_at: str | None = None

    parent_id: int | None = Field(
        default=None,
        gt=0,
    )


class UpdateTodoInput(BaseModel):
    todo_id: int = Field(
        gt=0,
    )

    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=200,
    )

    due_at: str | None = None


class TodoIdInput(BaseModel):
    todo_id: int = Field(
        gt=0,
    )


class SearchTodoInput(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=100,
    )
