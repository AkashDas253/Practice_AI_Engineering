# Evaluation & Testing Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

## Test Fundamentals

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `basic_llm_test.py` | Demonstrates testing a model against known inputs and expected outputs. | `python basic_llm_test.py` |
| `exact_match_evaluation.py` | Demonstrates evaluating deterministic outputs using exact and simple string matching strategies. | `python exact_match_evaluation.py` |
| `keyword_evaluation.py` | Demonstrates evaluating whether required keywords or concepts appear in a response. | `python keyword_evaluation.py` |
| `structured_output_evaluation.py` | Demonstrates evaluating whether model output satisfies a required schema and validation rules. | `python structured_output_evaluation.py` |
| `semantic_evaluation.py` | Demonstrates evaluating whether a response conveys the expected meaning rather than requiring identical wording. | `python semantic_evaluation.py` |

## Evaluation Methods

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `llm_judge_evaluation.py` | Demonstrates using an LLM to evaluate another model's response against defined criteria. | `python llm_judge_evaluation.py` |
| `rubric_evaluation.py` | Demonstrates evaluating a response against multiple independent evaluation criteria. | `python rubric_evaluation.py` |
| `response_quality_evaluation.py` | Demonstrates evaluating response quality across separate dimensions such as relevance, clarity, completeness, and correctness. | `python response_quality_evaluation.py` |
| `evaluation_metrics.py` | Demonstrates calculating aggregate evaluation metrics such as pass rate, average score, and failure rate. | `python evaluation_metrics.py` |

## Test Datasets & Batch Evaluation

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `test_dataset.py` | Demonstrates creating a reusable collection of inputs and evaluation expectations. | `python test_dataset.py` |
| `batch_evaluation.py` | Demonstrates running an evaluation across multiple test cases and collecting aggregate results. | `python batch_evaluation.py` |
| `test_edge_cases.py` | Demonstrates testing unusual, ambiguous, empty, malformed, and boundary inputs. | `python test_edge_cases.py` |
| `test_failure_cases.py` | Demonstrates testing cases where the system is expected to refuse, fail, or return an error. | `python test_failure_cases.py` |

## Regression & Consistency Testing

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `prompt_regression_test.py` | Demonstrates checking whether prompt changes affect previously passing test cases. | `python prompt_regression_test.py` |
| `consistency_testing.py` | Demonstrates evaluating whether repeated runs produce sufficiently consistent results for the same input. | `python consistency_testing.py` |
| `evaluation_baseline.py` | Demonstrates establishing an evaluation baseline before changing a model, prompt, retrieval strategy, or agent implementation. | `python evaluation_baseline.py` |
| `evaluation_comparison.py` | Demonstrates comparing two system versions against the same evaluation cases and criteria. | `python evaluation_comparison.py` |

## Tool & Agent Evaluation

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `tool_call_evaluation.py` | Demonstrates evaluating whether the correct tool was selected and appropriate arguments were generated. | `python tool_call_evaluation.py` |
| `tool_execution_evaluation.py` | Demonstrates evaluating whether tool execution produced the expected result and behavior. | `python tool_execution_evaluation.py` |
| `agent_trajectory_evaluation.py` | Demonstrates evaluating an agent's sequence of decisions, tool calls, and intermediate steps. | `python agent_trajectory_evaluation.py` |
| `agent_trajectory_live_evaluation.py` | Demonstrates evaluating the actual trajectory produced by a live agent, including its decisions, tool calls, and intermediate results. | `python agent_trajectory_live_evaluation.py` |
| `agent_task_evaluation.py` | Demonstrates evaluating whether an agent completed its intended task. | `python agent_task_evaluation.py` |

## RAG Evaluation

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `rag_retrieval_evaluation.py` | Demonstrates evaluating whether retrieval returned relevant and sufficient documents or chunks. | `python rag_retrieval_evaluation.py` |
| `rag_answer_evaluation.py` | Demonstrates evaluating whether a RAG answer is supported by the retrieved context. | `python rag_answer_evaluation.py` |

## Safety Evaluation

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `safety_evaluation.py` | Demonstrates testing whether a system handles defined unsafe or restricted scenarios according to expected behavior. | `python safety_evaluation.py` |

## End-to-End Evaluation

| Script Name | Purpose / Evaluation Concept | Execution Command |
| --- | --- | --- |
| `end_to_end_evaluation.py` | Demonstrates evaluating an entire AI pipeline from input through model response, tools, retrieval, and final output. | `python end_to_end_evaluation.py` |
