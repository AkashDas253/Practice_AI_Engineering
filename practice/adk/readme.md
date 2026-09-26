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

### State Management & Execution Control

| Practice Folder | Purpose / ADK Feature | Direct Python Command | ADK CLI Command |
| --- | --- | --- | --- |
| `sessions/` | Multi-turn conversation persistence and session history management.| `python sessions/main.py` | `adk run sessions` |
| `state_management/` | Reading, updating, and scoping variables in runtime session memory. | `python state_management/main.py` | `adk run state_management` |
| `streaming/` | Intercepting real-time token streams and intermediate generation events. | `python streaming/main.py` | `adk run streaming` |
| `callbacks/` | Hooking into pre/post execution events for models, agents, and tools. | `python callbacks/main.py` | `adk run callbacks` |

---

### Workflows & Multi-Agent Systems

| Practice Folder | Purpose / ADK Feature | Direct Python Command | ADK CLI Command |
| --- | --- | --- | --- |
| `sequential_workflow/` | Chaining agents sequentially where Agent A output feeds Agent B input.| `python sequential_workflow/main.py` | `adk run sequential_workflow` |
| `parallel_workflow/` | Executing independent sub-agents concurrently and merging results. | `python parallel_workflow/main.py` | `adk run parallel_workflow` |
| `loop_workflow/` | Iterative task execution loops for self-correction and refinement. | `python loop_workflow/main.py` | `adk run loop_workflow` |
| `sub_agents/` | Explicit task delegation from a coordinator agent to specialized sub-agents. | `python sub_agents/main.py` | `adk run sub_agents` |
| `multi_agent_system/` | Autonomous multi-agent coordination with dynamic routing. | `python multi_agent_system/main.py` | `adk run multi_agent_system` |

---

