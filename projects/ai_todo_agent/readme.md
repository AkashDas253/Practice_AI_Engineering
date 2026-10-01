# AI Todo Agent

A simple AI-powered Todo Agent built with Gemini Function Calling, Pydantic, and Python.

The agent can understand natural-language task requests and manage tasks, subtasks, due times, and reminders.

## Features

- Add tasks using natural language
- Create tasks with subtasks
- List and search tasks
- Update task titles and due times
- Complete tasks and subtasks
- Delete tasks and subtasks
- Schedule timed reminders
- Reminders work while the application is running
- Pydantic-based validation
- Gemini Function Calling
- Agent execution history
- Persistent Todo storage using JSON

## Project Structure

```
ai_todo_agent/
│
├── agent.py
├── config.py
├── main.py
├── models.py
├── output_store.py
├── reminder.py
├── todo_store.py
├── tools.py
│
├── .env
├── .env.example
├── .gitignore
├── requirements.txt
│
└── output/
    ├── todos.json
    └── history.jsonl
```

## Setup

Create and activate a virtual environment:

```
python -m venv .venv
```

Windows:

```
.venv\Scripts\activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Create `.env`:

```
GEMINI_API_KEY=your_gemini_api_key_here
```

## Run

```
python main.py
```

Example:

```
You: add learn FastAPI

Agent: Added "learn FastAPI".
```

## Subtasks

Tasks can contain subtasks.

```
You: create a trip preparation task with book hotel, buy tickets and pack bags as subtasks
```

The task structure can look like:

```
1. [ ] Trip preparation
   2. [ ] Book hotel
   3. [ ] Buy tickets
   4. [ ] Pack bags
```

## Timed Reminders

You can give a task a specific date and time:

```
You: remind me to buy bread today at 8:30 PM
```

The task is saved with a due time.

When the due time arrives, the running application displays:

```
🔔 REMINDER
Task: buy bread
Due: 2026-10-01 08:30 PM
```

Reminders work **only while `main.py` is running**.

If the application is closed, reminders are not triggered.

## Task Management

Examples:

```
add learn Python
```

```
show my tasks
```

```
find my Python tasks
```

```
complete task 2
```

```
change task 1 to learn FastAPI
```

```
change task 1 to tomorrow at 9 AM
```

```
delete task 3
```

```
clear completed tasks
```

## Storage

Todo data is stored in:

```
output/todos.json
```

AI execution history is stored in:

```
output/history.jsonl
```

The history file keeps the most recent 500 runs.

## Technologies

 - Python
- Google Gemini
- Gemini Function Calling
- Pydantic
- JSON / JSONL
- Threading

## Model

The project uses:

```
gemini-3.5-flash-lite
```
