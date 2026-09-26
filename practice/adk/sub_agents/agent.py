import warnings
warnings.filterwarnings("ignore")

from google.adk.agents import Agent

# Specify model
MODEL_ID = "gemini-3.5-flash-lite"

# Specialized Sub-agent 1: Tech Specialist
tech_agent = Agent(
    name="tech_specialist",
    model=MODEL_ID,
    instruction="You answer technical and programming questions concisely.",
    description="Specialist for technical and coding queries."
)

# Specialized Sub-agent 2: Math Specialist
math_agent = Agent(
    name="math_specialist",
    model=MODEL_ID,
    instruction="You perform math calculations and explain formulas concisely.",
    description="Specialist for math queries."
)

# Parent Coordinator Agent (Exposed as root_agent for ADK CLI)
root_agent = Agent(
    name="coordinator_agent",
    model=MODEL_ID,
    instruction=(
        "You are a dispatcher. Delegate technical queries to tech_specialist "
        "and math queries to math_specialist."
    ),
    sub_agents=[tech_agent, math_agent],
    description="Main coordinator delegating tasks to specialized sub-agents."
)