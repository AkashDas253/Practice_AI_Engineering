# Prompt Engineering Practice

Ensure `python-dotenv`, `google-genai`, and `pydantic` are installed, with your `GEMINI_API_KEY` configured in `.env` following the sctructure in `.env.example`.

| Script Name | Purpose / Use Case | Execution Command |
| --- | --- | --- |
| `zero_one_few_shot_prompting.py` | Compares 0-shot, 1-shot, and few-shot formatting and classification accuracy. | `python zero_one_few_shot_prompting.py` |
| `system_instructions_and_constraints.py` | Enforces persona rules, output length bounds, and negative constraints via config. | `python system_instructions_and_constraints.py` |
| `chain_of_thought_reasoning.py` | Forces explicit step-by-step logic in `<thinking>` tags to avoid reasoning errors. | `python chain_of_thought_reasoning.py` |
| `tree_of_thought_reasoning.py` | Explores multiple parallel reasoning branches before evaluating and picking the best strategy. | `python tree_of_thought_reasoning.py` |
| `prompt_chaining_pipeline.py` | Feeds output from an extraction stage directly into a recommendation stage. | `python prompt_chaining_pipeline.py` |
| `self_correction_and_critique.py` | Generates a response, critiques it against explicit constraints, and rewrites it. | `python self_correction_and_critique.py` |
| `meta_prompting_and_steering.py` | Expands raw user requests into engineered, structured system prompts before running. | `python meta_prompting_and_steering.py` |
| `structured_json_schema.py` | Forces strict JSON output adhering to a Pydantic schema using Gemini response config. | `python structured_json_schema.py` |
