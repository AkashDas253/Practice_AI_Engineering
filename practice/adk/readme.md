# ADK Practice

Ensure `google-adk`, `google-genai`, `python-dotenv`, and `pydantic` are installed in your Python environment. Configure your `GEMINI_API_KEY` in the local `.env` file located in your practice root directory (`adk_practice/.env`):

```env
GEMINI_API_KEY="your_actual_gemini_api_key_here"

```

Each practice module uses a dual-script architecture that isolates declarative agent configuration from programmatic runtime execution. The `agent.py` file exposes a `root_agent` using `models/gemini-3.6-flash` for the ADK CLI (`adk run`), while `main.py` imports `root_agent` and sets up an `InMemorySessionService` and `Runner` for direct script execution.

---

### Folder Pattern

```text
adk_practice/
├── .env
└── practice_agent/
    ├── agent.py   # Declarative agent configuration (Target for ADK CLI)
    └── main.py    # Runner, session, and test harness (Target for Direct Python)

```

---

### Core Fundamentals & Tooling

| Practice Folder | Purpose / ADK Feature | Direct Python Command | ADK CLI Command |
| --- | --- | --- | --- |
| `basic_agent/` | Core `Agent` declaration, model targeting, and single-turn interaction. | `python basic_agent/main.py` | `adk run basic_agent` |
| `agent_instructions/` | System instructions, persona steering, and task constraints. | `python agent_instructions/main.py` | `adk run agent_instructions` |
| `function_tools/` | Single custom Python function registration and model invocation. | `python function_tools/main.py` | `adk run function_tools` |
| `multiple_tools/` | Dynamic tool selection across multiple registered Python functions. | `python multiple_tools/main.py` | `adk run multiple_tools` |
| `tool_context/` | Accessing runtime state and session metadata inside tools via `ToolContext`. | `python tool_context/main.py` | `adk run tool_context` |

---
