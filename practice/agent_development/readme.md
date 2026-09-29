
# Agent Development Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

| Script Name | Purpose / Agent Concept | Execution Command |
| --- | --- | --- |
| `agent_basic_loop.py` | Demonstrates the basic agent loop: receive input, decide an action, execute it, observe the result, and continue. | `python agent_basic_loop.py` |
| `agent_state_management.py` | Demonstrates maintaining agent state across multiple steps and conversation turns. | `python agent_state_management.py` |
| `agent_context_management.py` | Demonstrates managing the context available to an agent across multiple steps. | `python agent_context_management.py` |
| `agent_planning.py` | Demonstrates breaking a complex task into smaller steps before execution. | `python agent_planning.py` |
| `agent_replanning.py` | Demonstrates updating or changing a plan when a step fails or produces an unexpected result. | `python agent_replanning.py` |
| `agent_goal_completion.py` | Demonstrates continuing an agent loop until a defined goal or completion condition is reached. | `python agent_goal_completion.py` |
| `agent_stop_conditions.py` | Demonstrates controlling when an agent should stop, including success, failure, iteration limits, and time limits. | `python agent_stop_conditions.py` |
| `agent_memory.py` | Demonstrates storing and reusing information across agent interactions. | `python agent_memory.py` |
| `agent_handoff.py` | Demonstrates transferring a task from one agent or specialized component to another. | `python agent_handoff.py` |
| `agent_multi_agent.py` | Demonstrates coordinating multiple specialized agents to complete a larger task. | `python agent_multi_agent.py` |
| `agent_human_in_the_loop.py` | Demonstrates pausing an agent for human input or approval before continuing execution. | `python agent_human_in_the_loop.py` |
| `agent_failure_recovery.py` | Demonstrates recovering from failed agent steps and deciding whether to retry, adapt, or stop. | `python agent_failure_recovery.py` |
| `agent_observability.py` | Demonstrates recording agent steps, decisions, tool calls, results, and errors for debugging and monitoring. | `python agent_observability.py` |
| `agent_evaluation.py` | Demonstrates evaluating whether an agent completed its task correctly and according to defined criteria. | `python agent_evaluation.py` |
