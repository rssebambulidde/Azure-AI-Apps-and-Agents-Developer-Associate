"""
Upgrade existing travel-assistant-demo agent to a new version

This script creates a NEW VERSION of the existing agent
without registering a new agent. Same agent name, better version.
"""

import os
import json
from pathlib import Path
from dotenv import load_dotenv

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    PromptAgentDefinition,
    OpenApiTool,
    OpenApiFunctionDefinition,
    OpenApiAnonymousAuthDetails,
)
from azure.identity import AzureCliCredential

# Load environment
env_file = Path(__file__).parent / ".env"
if env_file.exists():
    load_dotenv(env_file)

project_endpoint = os.getenv("PROJECT_ENDPOINT")
model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")

if not project_endpoint or not model_deployment_name:
    raise ValueError("PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be set in .env")

# Load OpenAPI spec
spec_path = Path(__file__).resolve().parents[1] / "cloudflare" / "worker" / "openapi.json"
with spec_path.open("r", encoding="utf-8") as f:
    openapi_spec = json.load(f)

# Create tool
travel_tools = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="travel_tools",
        description="Get weather and travel itinerary information for destinations",
        spec=openapi_spec,
        auth=OpenApiAnonymousAuthDetails(),
    )
)

# Enhanced instructions for production
production_instructions = """You are an expert travel consultant with deep knowledge of destinations worldwide.

YOUR ROLE:
- Plan comprehensive, practical travel itineraries
- Provide realistic budget estimates and cost breakdowns
- Give weather-appropriate packing recommendations
- Offer practical travel tips and safety advice

AVAILABLE TOOLS:
- Use the travel_tools API to get current weather information
- Use travel_tools to get curated itinerary suggestions

FORMATTING:
Structure your response in these sections:
1. ITINERARY - Day-by-day activities and attractions
2. WEATHER - Climate info and packing list
3. BUDGET - Estimated daily and total costs
4. PRACTICAL TIPS - Local insights, transportation, dining recommendations
5. SAFETY NOTES - Any important precautions

TONE & STYLE:
- Be friendly and encouraging
- Provide specific, actionable recommendations
- Balance budget considerations with experience quality
- Always use the tools to get accurate weather and itinerary data
- Be honest about budget feasibility

IMPORTANT:
- Always call both weather AND itinerary tools for any destination
- Use the tools to ground your recommendations in real data
- Mention specific activities, not generic advice
- Include local transport options and costs
- Provide honest budget assessments"""

print("\n" + "="*70)
print("UPGRADING EXISTING AGENT: travel-assistant-demo")
print("="*70)

with AzureCliCredential() as credential, AIProjectClient(
    endpoint=project_endpoint,
    credential=credential,
) as client:
    # Create new version of existing agent
    agent = client.agents.create_version(
        agent_name="travel-assistant-demo",
        definition=PromptAgentDefinition(
            model=model_deployment_name,
            instructions=production_instructions,
            tools=[travel_tools],
        ),
    )

    print(f"\n✅ AGENT UPGRADED SUCCESSFULLY!")
    print(f"   Agent Name: {agent.name}")
    print(f"   New Version: {agent.version}")
    print(f"   Status: Ready to serve travel requests")
    print(f"\n   Portal URL:")
    print(f"   {project_endpoint}/agents/{agent.name}")
    print("\n" + "="*70)
    print("WHAT CHANGED:")
    print("="*70)
    print("""
✓ Enhanced instructions with expert consultant role
✓ Better formatting (5-section structure)
✓ Mandatory tool usage (weather + itinerary)
✓ More detailed budget guidance
✓ Local transport & cost recommendations
✓ Honest budget assessments
✓ Specific activity recommendations
    """)
    print("="*70)
    print("NEXT STEPS:")
    print("="*70)
    print(f"""
1. Go to Foundry Portal
2. Open agent: {agent.name}
3. Test with prompt:
   "Plan a 3-day trip to Paris with $2000 budget"
4. View traces to see tool calls
5. Verify output has all 5 sections
    """)
    print("="*70 + "\n")
