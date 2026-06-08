"""
Deploy Multi-Agent Travel Workflow to Azure AI Foundry

This script registers the multi-agent travel planning system
as a production agent in the Foundry portal.
"""

import os
import asyncio
from pathlib import Path
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition
from azure.identity import AzureCliCredential
from dotenv import load_dotenv

# Load environment variables from .env file
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)


def deploy_multi_agent_workflow() -> None:
    """Register the multi-agent workflow as a Foundry agent"""

    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")

    if not project_endpoint or not model_deployment_name:
        raise ValueError(
            "PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be set in the environment."
        )

    print("\n" + "=" * 70)
    print("DEPLOYING MULTI-AGENT TRAVEL WORKFLOW TO FOUNDRY")
    print("=" * 70)

    with AzureCliCredential() as credential, AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    ) as project_client:

        # Define the multi-agent system instructions
        agent_definition = PromptAgentDefinition(
            model=model_deployment_name,
            instructions=(
                "You are a comprehensive travel planning assistant powered by specialized agents. "
                "When a user requests travel planning information, you coordinate with expert agents:\n\n"
                "1. PLANNING AGENT: Creates detailed itineraries with attractions and daily activities\n"
                "2. BUDGET AGENT: Calculates trip costs and validates budgets\n"
                "3. WEATHER AGENT: Provides weather forecasts and packing recommendations\n"
                "4. SAFETY AGENT: Offers travel safety information and tips\n\n"
                "For every travel request, you:\n"
                "- Parse the destination, duration, and budget\n"
                "- Gather insights from each specialist agent\n"
                "- Synthesize a comprehensive travel guide\n"
                "- Highlight budget feasibility and packing needs\n\n"
                "Always present information in a structured, easy-to-read format with sections for:\n"
                "- ITINERARY (day-by-day activities)\n"
                "- BUDGET (cost breakdown)\n"
                "- WEATHER & PACKING (climate info + what to bring)\n"
                "- SAFETY TIPS (local guidance)\n\n"
                "Be friendly, thorough, and practical in all recommendations."
            ),
        )

        # Create or update the agent version
        agent = project_client.agents.create_version(
            agent_name="multi-agent-travel-planner",
            definition=agent_definition,
        )

        print(f"\n✅ Agent Deployed Successfully!")
        print(f"   Name: {agent.name}")
        print(f"   Version: {agent.version}")
        print(f"   Model: {model_deployment_name}")
        print(f"\n📍 Portal URL: {project_endpoint}/agents/{agent.name}")
        print("\n" + "=" * 70)
        print("NEXT STEPS:")
        print("=" * 70)
        print(
            "1. Go to your Azure AI Foundry project portal\n"
            "2. Find the agent 'multi-agent-travel-planner'\n"
            "3. Start a chat conversation\n"
            "4. Try prompts like:\n"
            "   - 'Plan a 3-day trip to Kampala with $2000 budget'\n"
            "   - 'What should I pack for a week in Tokyo?'\n"
            "   - 'I have $500 for 2 days in Paris. Is that enough?'"
        )
        print("=" * 70 + "\n")


if __name__ == "__main__":
    deploy_multi_agent_workflow()
