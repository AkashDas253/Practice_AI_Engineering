
# Tooling & Function Calling Practice

 Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

| Script Name | Purpose / Gemini Feature | Execution Command |
| --- | --- | --- |
| `single_tool_function_calling.py` | Demonstrates the basic tool-calling lifecycle: model requests a tool, the application executes it, and the result is returned to the model. | `python single_tool_function_calling.py` |
| `multi_tool_routing.py` | Demonstrates tool selection/routing: the model selects the appropriate tool from multiple available tools. | `python multi_tool_routing.py` |
| `manual_tool_handling.py` | Demonstrates manual tool orchestration: inspect tool calls, execute the requested tools, and explicitly return their results. | `python manual_tool_handling.py` |
| `tool_call_mode_configuration.py` | Demonstrates controlling tool-calling behavior, including when tools may or must be used. | `python tool_call_mode_configuration.py` |
| `pydantic_structured_tools.py` | Demonstrates structured tool inputs and schemas using typed Pydantic models for complex parameters. | `python pydantic_structured_tools.py` |
| `agent_react_loop.py` | Demonstrates an iterative agent loop combining model decisions, tool execution, tool results, instructions, and conversation state. | `python agent_react_loop.py` |
| `parallel_tool_calls.py` | Demonstrates multiple independent tool calls requested within a single model turn. | `python parallel_tool_calls.py` |
| `tool_error_handling.py` | Demonstrates tool error handling, including invalid arguments, missing data, execution failures, and structured error results returned to the model. | `python tool_error_handling.py` |
| `tool_confirmation.py` | Demonstrates human-in-the-loop control by requiring approval before executing sensitive or consequential tools. | `python tool_confirmation.py` |
| `manual_react_agent.py` | Demonstrates full manual agent/tool orchestration: model response, tool calls, execution, tool results, and the iterative loop. | `python manual_react_agent.py` |
| `tool_argument_validation.py` | Demonstrates validating model-generated tool arguments before execution, including type, range, format, and business-rule validation. | `python tool_argument_validation.py` |
| `tool_result_validation.py` | Demonstrates validating tool outputs before sending them back to the model. | `python tool_result_validation.py` |
| `tool_retry_timeout.py` | Demonstrates handling temporary tool failures, timeouts, and controlled retries. | `python tool_retry_timeout.py` |
| `tool_authorization.py` | Demonstrates checking whether the current user/application is authorized to execute a requested tool before execution. | `python tool_authorization.py` |
| `sequential_tool_dependencies.py` | Demonstrates dependent tool calls where the result of one tool determines the arguments or necessity of the next tool. | `python sequential_tool_dependencies.py` |
| `tool_call_ids_and_correlation.py` | Demonstrates associating tool results with the specific tool-call request they belong to, especially when multiple calls are in flight. | `python tool_call_ids_and_correlation.py` |