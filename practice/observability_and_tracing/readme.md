# Observability and Tracing Practice

Ensure `python-dotenv` and `google-genai` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

## Logging Fundamentals

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `basic_logging.py` | Demonstrates recording basic application, model, tool, and agent events. | `python basic_logging.py` |
| `structured_logging.py` | Demonstrates recording logs as structured data instead of plain text. | `python structured_logging.py` |
| `request_tracking.py` | Demonstrates assigning identifiers to requests so related events can be correlated. | `python request_tracking.py` |

## Tracing Fundamentals

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `tool_call_tracing.py` | Demonstrates tracing tool requests, arguments, execution, results, and errors. | `python tool_call_tracing.py` |
| `agent_step_tracing.py` | Demonstrates tracing individual steps in an agent execution loop. | `python agent_step_tracing.py` |
| `trace_context.py` | Demonstrates carrying trace context across model calls, tools, and agent steps. | `python trace_context.py` |
| `nested_spans.py` | Demonstrates representing an agent operation as a parent trace containing nested model and tool operations. | `python nested_spans.py` |

## Performance and Usage

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `latency_tracking.py` | Demonstrates measuring model, tool, and end-to-end execution latency. | `python latency_tracking.py` |
| `token_usage_tracking.py` | Demonstrates recording model token usage across requests and conversations. | `python token_usage_tracking.py` |
| `cost_tracking.py` | Demonstrates estimating and recording model usage costs from tracked usage data. | `python cost_tracking.py` |

## Reliability and Errors

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `error_tracking.py` | Demonstrates recording and correlating model, tool, and application errors. | `python error_tracking.py` |
| `retry_tracking.py` | Demonstrates recording retries, retry reasons, attempts, and final outcomes. | `python retry_tracking.py` |

## Agent and Conversation Observability

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `agent_execution_trace.py` | Demonstrates producing a complete trace of an agent's decisions, tools, observations, and final result. | `python agent_execution_trace.py` |
| `conversation_tracing.py` | Demonstrates tracing multiple model turns while maintaining a conversation-level identifier. | `python conversation_tracing.py` |
| `tool_result_observability.py` | Demonstrates recording tool outputs and execution metadata for debugging and analysis. | `python tool_result_observability.py` |
| `context_usage_tracking.py` | Demonstrates tracking the context supplied to the model across agent steps. | `python context_usage_tracking.py` |

## Safety and Privacy

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `guardrail_observability.py` | Demonstrates recording guardrail checks, decisions, blocked actions, and failures. | `python guardrail_observability.py` |
| `sensitive_data_logging.py` | Demonstrates preventing or redacting sensitive information from application logs and traces. | `python sensitive_data_logging.py` |

## Trace Management

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `trace_sampling.py` | Demonstrates recording only selected traces when full tracing would create excessive overhead or volume. | `python trace_sampling.py` |
| `trace_export.py` | Demonstrates exporting collected traces and events to an external observability system or file. | `python trace_export.py` |

## Metrics and Monitoring

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `observability_dashboard_data.py` | Demonstrates aggregating traces and logs into metrics useful for monitoring agent performance. | `python observability_dashboard_data.py` |

## End-to-End

| Script Name | Purpose / Observability Concept | Execution Command |
| --- | --- | --- |
| `end_to_end_observability.py` | Demonstrates tracing an entire AI application from user request through model calls, tools, guardrails, and final response. | `python end_to_end_observability.py` |

