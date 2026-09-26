import warnings
warnings.filterwarnings("ignore")

from google.adk.agents import Agent

# Specify model
MODEL_ID = "gemini-3.5-flash-lite"

# Specialist 1: Technical Support
tech_agent = Agent(
    name="tech_support_agent",
    model=MODEL_ID,
    instruction="Provide concise troubleshooting steps for system errors, software bugs, and networking issues.",
    description="Specialist for technical errors, software bugs, API issues, and hardware troubleshooting."
)

# Specialist 2: Billing & Subscriptions
billing_agent = Agent(
    name="billing_agent",
    model=MODEL_ID,
    instruction="Help users resolve billing disputes, explain subscription tiers, and provide refund policies.",
    description="Specialist for payment issues, double charges, invoices, and subscription plans."
)

# Specialist 3: Creative Copywriting
creative_agent = Agent(
    name="creative_agent",
    model=MODEL_ID,
    instruction="Generate engaging marketing copy, slogans, and creative content concisely.",
    description="Specialist for creative writing, slogan generation, and promotional marketing text."
)

# Root Coordinator Agent with Dynamic Multi-Agent Routing
root_agent = Agent(
    name="triage_router",
    model=MODEL_ID,
    instruction=(
        "You are an autonomous triage router. Dynamically evaluate incoming queries "
        "and route control to the appropriate specialist:\n"
        "- Route technical failures or software bugs to tech_support_agent.\n"
        "- Route payments, invoices, or refund requests to billing_agent.\n"
        "- Route copywriting, slogan, or creative requests to creative_agent."
    ),
    sub_agents=[tech_agent, billing_agent, creative_agent],
    description="Autonomous multi-agent triage coordinator with dynamic request routing."
)