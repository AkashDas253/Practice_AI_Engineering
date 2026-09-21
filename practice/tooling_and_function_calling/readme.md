
# Tooling & Function Calling Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

| Script Name | Purpose / Gemini Feature | Execution Command |
| --- | --- | --- |
| `single_tool_function_calling.py` | Demonstrates automatic execution of a single custom Python tool function. | `python single_tool_function_calling.py` |
| `multi_tool_routing.py` | Registers multiple tool functions and lets Gemini dynamically select the correct tool. | `python multi_tool_routing.py` |
| `manual_tool_handling.py` | Disables AFC to manually inspect `FunctionCall` objects and submit `FunctionResponse`. | `python manual_tool_handling.py` |
| `tool_call_mode_configuration.py` | Controls tool calling behavior (`mode="ANY"`, `mode="AUTO"`) using `types.ToolConfig`. | `python tool_call_mode_configuration.py` |
| `pydantic_structured_tools.py` | Uses Pydantic models to construct complex function parameters. | `python pydantic_structured_tools.py` |
| `agent_react_loop.py` | Implements a multi-turn ReAct agent loop combining tools, instructions, and chat state. | `python agent_react_loop.py` |