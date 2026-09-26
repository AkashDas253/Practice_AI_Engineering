import warnings
warnings.filterwarnings("ignore")

from google.adk.agents import Agent, SequentialAgent

# Specify model
model="gemini-3.5-flash-lite"

# Step 1 Agent: Generates a raw outline
outline_agent = Agent(
    name="outline_agent",
    model=model,
    instruction="Given a topic, create a simple 3-point outline. Be brief.",
    description="Generates a raw topic outline."
)

# Step 2 Agent: Takes output from Step 1 and refines it
editor_agent = Agent(
    name="editor_agent",
    model=model,
    instruction="Take the previous outline and format it into professional, clear bullet points with short explanations.",
    description="Refines and formats an existing outline."
)

# Sequential Workflow Orchestrator (Exposed as root_agent for ADK CLI)
root_agent = SequentialAgent(
    name="sequential_workflow_agent",
    sub_agents=[outline_agent, editor_agent],
    description="Executes outline creation followed by editor refinement sequentially."
)