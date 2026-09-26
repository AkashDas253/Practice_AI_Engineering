import warnings
warnings.filterwarnings("ignore")

from google.adk.agents import Agent, ParallelAgent

# Specify model
MODEL_ID = "gemini-3.5-flash-lite"

# Independent Sub-agent 1: Analyzes Advantages
pros_agent = Agent(
    name="pros_agent",
    model=MODEL_ID,
    instruction="List exactly 2 key advantages/pros of the subject. Be concise.",
    description="Analyzes advantages."
)

# Independent Sub-agent 2: Analyzes Disadvantages
cons_agent = Agent(
    name="cons_agent",
    model=MODEL_ID,
    instruction="List exactly 2 key disadvantages/cons of the subject. Be concise.",
    description="Analyzes disadvantages."
)

# Parallel Workflow Orchestrator (Exposed as root_agent for ADK CLI)
root_agent = ParallelAgent(
    name="parallel_workflow_agent",
    sub_agents=[pros_agent, cons_agent],
    description="Executes pros and cons analysis concurrently."
)