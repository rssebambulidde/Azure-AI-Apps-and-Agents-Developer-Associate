import os
import asyncio
import json
from pathlib import Path
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    OpenApiAnonymousAuthDetails,
    OpenApiFunctionDefinition,
    OpenApiTool,
    PromptAgentDefinition,
)
from azure.identity import AzureCliCredential
from pydantic import Field


@tool(approval_mode="never_require")
def get_weather(
    city: Annotated[str, Field(description="The city to check weather for.")],
) -> str:
    """
    Get current weather information for a travel destination.
    Use this to provide accurate weather info and packing recommendations.
    """
    weather_map = {
        "paris": "Mild and cloudy, around 18°C with a light breeze. Pack layers and a light jacket.",
        "tokyo": "Cool and dry, around 16°C with clear skies. Perfect weather for walking tours.",
        "sydney": "Warm and sunny, around 24°C. Sunscreen and light clothing recommended.",
        "rome": "Pleasant and sunny, around 21°C. Great for outdoor sightseeing.",
        "kampala": "Warm and tropical, around 24°C with possible afternoon rain. Pack a rain jacket.",
    }
    weather = weather_map.get(city.lower())
    if weather:
        return f"Weather in {city}: {weather}"
    return f"Weather information for {city} is not available in this demo. Assume temperate climate."


@tool(approval_mode="never_require")
def create_itinerary(
    city: Annotated[str, Field(description="The destination city.")],
    days: Annotated[int, Field(description="How many days the trip should last.")],
) -> str:
    """
    Create a day-by-day travel itinerary for a destination.
    Includes major attractions, cultural sites, and local experiences.
    """
    itineraries = {
        "paris": {
            1: "Explore the Eiffel Tower and Latin Quarter.",
            2: "Visit the Louvre Museum and walk along the Seine.",
            3: "Explore Montmartre, visit Notre-Dame, and enjoy cafes.",
            4: "Day trip to Versailles Palace.",
        },
        "tokyo": {
            1: "Explore Shibuya Crossing and Shinjuku district.",
            2: "Visit Senso-ji Temple and enjoy traditional Tokyo.",
            3: "Experience Tokyo Skytree and modern attractions.",
        },
        "sydney": {
            1: "Visit Sydney Opera House and Harbour Bridge.",
            2: "Explore Bondi Beach and coastal walks.",
            3: "Visit Blue Mountains or Taronga Zoo.",
        },
        "kampala": {
            1: "Explore city center and visit local markets.",
            2: "Tour Uganda Museum and Kasubi Tombs.",
            3: "Relax in city parks and shop at local markets.",
        },
    }
    
    city_itinerary = itineraries.get(city.lower(), {})
    if city_itinerary:
        result = f"Itinerary for {city} ({days} days):\n"
        for day in range(1, min(days + 1, 4)):
            activity = city_itinerary.get(day, f"Day {day}: Local exploration and leisure activities.")
            result += f"Day {day}: {activity}\n"
        return result
    
    return (
        f"Suggested itinerary for {city} ({days} days):\n"
        f"Day 1: Explore the city center and local attractions.\n"
        f"Day 2: Visit historical sites and cultural landmarks.\n"
        f"Day 3: Enjoy outdoor activities and local cuisine.\n"
        f"(Customize based on your interests and available time)"
    )


def register_foundry_agent() -> None:
    """Create a production travel assistant in the Azure AI Foundry project."""
    project_endpoint = os.getenv("PROJECT_ENDPOINT")
    model_deployment_name = os.getenv("MODEL_DEPLOYMENT_NAME")

    if not project_endpoint or not model_deployment_name:
        raise ValueError("PROJECT_ENDPOINT and MODEL_DEPLOYMENT_NAME must be set in the environment.")

    spec_path = Path(__file__).resolve().parents[1] / "cloudflare" / "worker" / "openapi.json"
    with spec_path.open("r", encoding="utf-8") as f:
        openapi_spec = json.load(f)

    travel_tools = OpenApiTool(
        openapi=OpenApiFunctionDefinition(
            name="travel_tools",
            description="Get weather and travel itinerary information for destinations",
            spec=openapi_spec,
            auth=OpenApiAnonymousAuthDetails(),
        )
    )

    # Enhanced production instructions
    production_instructions = (
        "You are an expert travel consultant with deep knowledge of destinations worldwide.\n\n"
        "YOUR ROLE:\n"
        "- Plan comprehensive, practical travel itineraries\n"
        "- Provide realistic budget estimates and cost breakdowns\n"
        "- Give weather-appropriate packing recommendations\n"
        "- Offer practical travel tips and safety advice\n\n"
        "AVAILABLE TOOLS:\n"
        "- Use the travel_tools API to get current weather information\n"
        "- Use travel_tools to get curated itinerary suggestions\n\n"
        "FORMATTING:\n"
        "Structure your response in these sections:\n"
        "1. ITINERARY - Day-by-day activities and attractions\n"
        "2. WEATHER - Climate info and packing list\n"
        "3. BUDGET - Estimated daily and total costs\n"
        "4. PRACTICAL TIPS - Local insights, transportation, dining recommendations\n"
        "5. SAFETY NOTES - Any important precautions\n\n"
        "TONE & STYLE:\n"
        "- Be friendly and encouraging\n"
        "- Provide specific, actionable recommendations\n"
        "- Balance budget considerations with experience quality\n"
        "- Always use the tools to get accurate weather and itinerary data\n"
        "- Be honest about budget feasibility"
    )

    with AzureCliCredential() as credential, AIProjectClient(
        endpoint=project_endpoint,
        credential=credential,
    ) as project_client:
        agent = project_client.agents.create_version(
            agent_name="travel-assistant",
            definition=PromptAgentDefinition(
                model=model_deployment_name,
                instructions=production_instructions,
                tools=[travel_tools],
            ),
        )
        print(f"✅ Registered Production Agent!")
        print(f"   Name: {agent.name}")
        print(f"   Version: {agent.version}")
        print(f"   Status: Ready to serve travel requests")


async def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    print("\n" + "="*70)
    print("TRAVEL ASSISTANT - PRODUCTION AGENT")
    print("="*70)
    print("\nRegistering agent in Azure AI Foundry...")
    register_foundry_agent()
    
    print("\n" + "-"*70)
    print("LOCAL TRAVEL PLANNING")
    print("-"*70 + "\n")
    
    city = input("Which city are you visiting? ").strip()
    days_input = input("How many days is your trip? ").strip()

    try:
        days_value = int(days_input)
        if days_value < 1 or days_value > 365:
            print("❌ Please enter a valid number of days (1-365).")
            return
    except ValueError:
        print("❌ Please enter a valid number.")
        return

    print(f"\n🌍 Planning {days_value}-day trip to {city}...")
    await process_trip_request(city, days_value)


async def process_trip_request(city: str, days: int):
    """Process travel request locally using the Agent Framework."""
    credential = AzureCliCredential()

    expert_instructions = (
        "You are an expert travel consultant. Your goal is to create a comprehensive, "
        "practical travel guide that helps travelers plan successfully.\n\n"
        "ALWAYS:\n"
        "1. Call the weather tool for current weather information\n"
        "2. Call the itinerary tool for curated activities\n"
        "3. Provide specific, actionable recommendations\n"
        "4. Format output clearly with: ITINERARY | WEATHER & PACKING | BUDGET | TIPS\n\n"
        "Be friendly, practical, and specific."
    )

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=expert_instructions,
        tools=[get_weather, create_itinerary],
    ) as agent:
        try:
            prompt = (
                f"Create a comprehensive travel guide for {city} for {days} days.\n"
                f"1. Get the weather using the weather tool\n"
                f"2. Create an itinerary using the itinerary tool\n"
                f"3. Provide packing recommendations based on weather\n"
                f"4. Suggest a realistic budget\n"
                f"5. Add practical travel tips\n\n"
                f"Format the response with clear sections."
            )
            response = await agent.run([prompt])
            print("\n" + "="*70)
            print("TRAVEL GUIDE")
            print("="*70 + "\n")
            print(response)
            print("\n" + "="*70)
        except Exception as exc:
            print(f"❌ Error: {exc}")


if __name__ == "__main__":
    asyncio.run(main())
