
# Structured Outputs & Validation Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in the local `.env` file.

## Structured Output Fundamentals

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `basic_structured_output.py` | Demonstrates requesting model responses as structured data instead of free-form text. | `python basic_structured_output.py` |
| `schema_definition.py` | Demonstrates defining an explicit schema that describes the expected structure and types of model output. | `python schema_definition.py` |
| `pydantic_output.py` | Demonstrates mapping structured model output into typed application models using Pydantic. | `python pydantic_output.py` |

## Data Structures

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `nested_structured_output.py` | Demonstrates validating nested objects and hierarchical structured responses. | `python nested_structured_output.py` |
| `list_structured_output.py` | Demonstrates generating and validating collections of structured objects. | `python list_structured_output.py` |
| `optional_fields.py` | Demonstrates distinguishing required, optional, nullable, and missing fields in structured data. | `python optional_fields.py` |

## Field & Semantic Validation

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `field_constraints.py` | Demonstrates enforcing field-level constraints such as types, enums, numeric ranges, string formats, and lengths. | `python field_constraints.py` |
| `cross_field_validation.py` | Demonstrates validating relationships and dependencies between multiple fields. | `python cross_field_validation.py` |
| `business_rule_validation.py` | Demonstrates applying application-specific business rules after structural and field-level validation. | `python business_rule_validation.py` |

## Parsing & Validation Handling

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `output_parsing.py` | Demonstrates converting raw model responses into application-usable structured data while handling parsing failures. | `python output_parsing.py` |
| `validation_error_handling.py` | Demonstrates detecting validation failures and handling invalid model output without crashing the application. | `python validation_error_handling.py` |
| `strict_output_validation.py` | Demonstrates using fail-closed validation to reject data that does not completely satisfy required constraints. | `python strict_output_validation.py` |
| `partial_output_handling.py` | Demonstrates safely handling incomplete or unusable structured responses without silently treating missing data as valid. | `python partial_output_handling.py` |

## Recovery & Resilience

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `structured_output_retry.py` | Demonstrates retrying generation when structured output fails validation with bounded retry attempts. | `python structured_output_retry.py` |
| `structured_output_repair.py` | Demonstrates repairing recoverable structured-data errors and re-validating the repaired result before use. | `python structured_output_repair.py` |
| `structured_output_defaults.py` | Demonstrates applying explicit and safe defaults to intentionally optional fields while preserving validation semantics. | `python structured_output_defaults.py` |

## Structured Output Integration

| Script Name | Purpose / Structured Output Concept | Execution Command |
| --- | --- | --- |
| `structured_output_pipeline.py` | Demonstrates the complete workflow: generate → parse → validate → recover or reject → use validated data. | `python structured_output_pipeline.py` |

