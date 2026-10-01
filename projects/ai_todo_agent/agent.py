from datetime import datetime

from google.genai import types

from config import (
    MAX_AGENT_STEPS,
    TODO_AGENT_MODEL,
    client,
)

from tools import (
    add_todo_tool,
    clear_completed_todos_tool,
    complete_todo_tool,
    delete_todo_tool,
    list_subtasks_tool,
    list_todos_tool,
    search_todos_tool,
    update_todo_tool,
)


def get_local_datetime() -> str:
    return datetime.now().astimezone().isoformat()


def build_system_instruction() -> str:

    current_time = get_local_datetime()

    return f"""
You are a reliable AI Todo Assistant.

Current local date and time:
{current_time}

You help users manage tasks, subtasks, and scheduled
tasks.

AVAILABLE OPERATIONS:

- Add a task
- Add a subtask
- List tasks
- List subtasks
- Search tasks
- Update a task
- Complete a task
- Delete a task
- Clear completed tasks

RULES:

1. ALWAYS use tools when reading or changing todo data.

2. NEVER claim an operation succeeded unless the
   corresponding tool returned success=true.

3. If a tool returns success=false, explain the
   failure briefly.

4. A top-level task has parent_id=null.

5. A subtask has parent_id set to its parent task ID.

6. If the user requests a task with multiple subtasks,
   create the parent first and use its returned ID
   for the subtasks.

7. Treat phrases such as:
   "remember this",
   "save this",
   "I need to",
   "add a task",
   "remind me",
   as task requests.

8. Relative dates such as "today", "tomorrow",
   "Friday", and "next week" should be interpreted
   using the current local date and time.

9. Convert scheduled times to ISO 8601 datetime values.

10. Do not invent a time if the user gives only a date.

11. If the user says "done", "finished", or "completed",
    use complete_todo.

12. If the user refers to a task by ID, use that ID.

13. If the user asks to change a task title, use
    update_todo.

14. If the user asks to change a due date/time, use
    update_todo.

15. Deleting a parent task also deletes its subtasks.

16. Keep normal responses concise and friendly.

17. Format task lists clearly.

18. If the request is unrelated to task management,
    explain that you are a Todo Assistant.
"""


# Gemini function declarations.

TOOLS = [
    types.Tool(
        function_declarations=[

            types.FunctionDeclaration(
                name="add_todo",
                description=(
                    "Create a task or subtask. "
                    "Use parent_id for a subtask. "
                    "due_at is an optional ISO 8601 "
                    "datetime."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "title": types.Schema(
                            type="STRING",
                            description="Task title.",
                        ),
                        "due_at": types.Schema(
                            type="STRING",
                            description=(
                                "Optional ISO 8601 "
                                "due date/time."
                            ),
                            nullable=True,
                        ),
                        "parent_id": types.Schema(
                            type="INTEGER",
                            description=(
                                "Parent task ID. "
                                "Use null for a "
                                "top-level task."
                            ),
                            nullable=True,
                        ),
                    },
                    required=["title"],
                ),
            ),

            types.FunctionDeclaration(
                name="list_todos",
                description=(
                    "List all tasks and subtasks."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={},
                ),
            ),

            types.FunctionDeclaration(
                name="list_subtasks",
                description=(
                    "List subtasks belonging to "
                    "a parent task."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "parent_id": types.Schema(
                            type="INTEGER",
                            description="Parent task ID.",
                        ),
                    },
                    required=["parent_id"],
                ),
            ),

            types.FunctionDeclaration(
                name="search_todos",
                description=(
                    "Search tasks and subtasks "
                    "by title."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "query": types.Schema(
                            type="STRING",
                            description="Search text.",
                        ),
                    },
                    required=["query"],
                ),
            ),

            types.FunctionDeclaration(
                name="update_todo",
                description=(
                    "Update a task title and/or "
                    "due date/time."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "todo_id": types.Schema(
                            type="INTEGER",
                            description="Todo ID.",
                        ),
                        "title": types.Schema(
                            type="STRING",
                            description=(
                                "New title. Optional."
                            ),
                            nullable=True,
                        ),
                        "due_at": types.Schema(
                            type="STRING",
                            description=(
                                "New ISO 8601 "
                                "due date/time. "
                                "Optional."
                            ),
                            nullable=True,
                        ),
                    },
                    required=["todo_id"],
                ),
            ),

            types.FunctionDeclaration(
                name="complete_todo",
                description=(
                    "Mark a task or subtask as completed."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "todo_id": types.Schema(
                            type="INTEGER",
                            description="Todo ID.",
                        ),
                    },
                    required=["todo_id"],
                ),
            ),

            types.FunctionDeclaration(
                name="delete_todo",
                description=(
                    "Delete a task and its subtasks."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "todo_id": types.Schema(
                            type="INTEGER",
                            description="Todo ID.",
                        ),
                    },
                    required=["todo_id"],
                ),
            ),

            types.FunctionDeclaration(
                name="clear_completed_todos",
                description=(
                    "Delete all completed tasks "
                    "and their subtasks."
                ),
                parameters=types.Schema(
                    type="OBJECT",
                    properties={},
                ),
            ),
        ]
    )
]


# Tool dispatcher.

def execute_tool(
    name: str,
    arguments: dict,
) -> dict:

    try:

        if name == "add_todo":

            return add_todo_tool(
                title=arguments["title"],
                due_at=arguments.get("due_at"),
                parent_id=arguments.get("parent_id"),
            )

        if name == "list_todos":
            return list_todos_tool()

        if name == "list_subtasks":

            return list_subtasks_tool(
                parent_id=arguments["parent_id"]
            )

        if name == "search_todos":

            return search_todos_tool(
                query=arguments["query"]
            )

        if name == "update_todo":

            return update_todo_tool(
                todo_id=arguments["todo_id"],
                title=arguments.get("title"),
                due_at=arguments.get("due_at"),
            )

        if name == "complete_todo":

            return complete_todo_tool(
                todo_id=arguments["todo_id"]
            )

        if name == "delete_todo":

            return delete_todo_tool(
                todo_id=arguments["todo_id"]
            )

        if name == "clear_completed_todos":

            return clear_completed_todos_tool()

        return {
            "success": False,
            "error": f"Unknown tool: {name}",
        }

    except Exception as error:

        return {
            "success": False,
            "error": str(error),
        }


# Agent execution.

def run_agent(
    user_message: str,
    history: list[types.Content] | None = None,
) -> tuple[str, list[types.Content], dict]:

    contents = list(
        history or []
    )

    contents.append(
        types.Content(
            role="user",
            parts=[
                types.Part(
                    text=user_message
                )
            ],
        )
    )

    trace = []

    for step in range(
        1,
        MAX_AGENT_STEPS + 1,
    ):

        response = client.models.generate_content(
            model=TODO_AGENT_MODEL,
            contents=contents,
            config=types.GenerateContentConfig(
                system_instruction=(
                    build_system_instruction()
                ),
                tools=TOOLS,
            ),
        )

        if not response.candidates:

            return (
                "I couldn't generate a response.",
                contents,
                {
                    "steps": step,
                    "trace": trace,
                },
            )

        model_content = (
            response.candidates[0].content
        )

        contents.append(
            model_content
        )

        function_calls = [
            part.function_call
            for part in model_content.parts
            if part.function_call
        ]

        if not function_calls:

            final_text = (
                response.text
                or "I couldn't generate a response."
            )

            return (
                final_text,
                contents,
                {
                    "steps": step,
                    "trace": trace,
                },
            )

        tool_response_parts = []

        for function_call in function_calls:

            arguments = dict(
                function_call.args or {}
            )

            result = execute_tool(
                name=function_call.name,
                arguments=arguments,
            )

            trace.append(
                {
                    "step": step,
                    "tool": function_call.name,
                    "arguments": arguments,
                    "success": result.get(
                        "success",
                        False,
                    ),
                }
            )

            tool_response_parts.append(
                types.Part.from_function_response(
                    name=function_call.name,
                    response=result,
                )
            )

        contents.append(
            types.Content(
                role="user",
                parts=tool_response_parts,
            )
        )

    return (
        "I couldn't complete that request.",
        contents,
        {
            "steps": MAX_AGENT_STEPS,
            "trace": trace,
        },
    )
