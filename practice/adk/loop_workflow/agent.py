import warnings
warnings.filterwarnings("ignore")

from google.adk.agents import Agent, LoopAgent

# Specify model
MODEL_ID = "gemini-3.5-flash-lite"

# Sub-agent 1: Draft Generator
draft_agent = Agent(
    name="draft_agent",
    model=MODEL_ID,
    instruction="Write a single concise marketing headline based on the user request.",
    description="Drafts initial headlines."
)

# Sub-agent 2: Critic and Refiner
critic_agent = Agent(
    name="critic_agent",
    model=MODEL_ID,
    instruction="Critique the headline provided in the current context and output an improved, punchier version.",
    description="Critiques and refines existing headlines."
)

# Loop Workflow Orchestrator (Exposed as root_agent for ADK CLI)
root_agent = LoopAgent(
    name="loop_workflow_agent",
    sub_agents=[draft_agent, critic_agent],
    max_iterations=2,
    description="Iteratively drafts, critiques, and refines headlines."
)