
# Gemini Basics Practice

 Ensure `python-dotenv`, `google-genai`, `pydantic`, and `pillow` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file inside the `gemini_basics` directory.

 | Script Name | Purpose / Gemini Feature | Execution Command |
| --- | --- | --- |
| `model_capabilities_inspector.py` | Lists available models and their exposed capabilities, limits, and supported actions. | `python model_capabilities_inspector.py` |
| `text_generation_and_config.py` | Introduces basic text generation and generation configuration such as temperature, top-p, top-k, and stop sequences. | `python text_generation_and_config.py` |
| `token_counting.py` | Counts input tokens before generation using `client.models.count_tokens()`. | `python token_counting.py` |
| `chat_history_and_sessions.py` | Demonstrates chat sessions, conversation history, and multi-turn interactions. | `python chat_history_and_sessions.py` |
| `streaming_chat_responses.py` | Handles real-time token streaming using `chat.send_message_stream()`. | `python streaming_chat_responses.py` |
| `structured_output.py` | Demonstrates structured JSON output using Pydantic schemas, including simple, nested, list, enum, optional, and complex structures. | `python structured_output.py` |
| `multimodal_images_and_media.py` | Sends images and other media to Gemini, including multiple images, structured output, token counting, streaming, and multimodal chat. | `python multimodal_images_and_media.py` |
| `function_calling_basics.py` | Uses custom Python functions as Gemini tools, including automatic and manual function calling, multiple tools, arguments, and function-call details. | `python function_calling_basics.py` |
| `code_execution_tool.py` | Uses Gemini's built-in Python code execution tool to generate and run code, inspect execution results, and view chat and response details. | `python code_execution_tool.py` |
| `grounding_google_search.py` | Uses Gemini's built-in Google Search grounding for up-to-date information and shows the grounded response, response details, token usage, and quota errors. | `python grounding_google_search.py` |


