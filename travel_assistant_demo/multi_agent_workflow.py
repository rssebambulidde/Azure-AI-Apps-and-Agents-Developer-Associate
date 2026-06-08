"""
Multi-Agent Workflow for Travel Planning

Specialized agents collaborate to create comprehensive travel guides:
- Planning Agent: Creates itineraries
- Budget Agent: Calculates costs
- Weather Agent: Provides weather info
- Safety Agent: Travel advisories
- Coordinator Agent: Orchestrates all agents
"""

import asyncio
import os
from typing import Annotated

from agent_framework import Agent, tool
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential
from pydantic import Field


# ============================================================================
# SHARED DATA & TOOLS
# ============================================================================

CITY_DATA = {
    "kampala": {
        "weather": "Warm and tropical, around 24°C with possible afternoon rain.",
        "budget_per_day": 80,  # USD
        "attractions": [
            "Nakasero and Owino Markets",
            "Independence Monument",
            "Uganda Museum",
            "Kasubi Tombs (UNESCO)",
            "Gaddafi National Mosque",
        ],
        "safety": "Generally safe for tourists. Avoid walking alone at night.",
    },
    "paris": {
        "weather": "Mild and cloudy, around 18°C with a light breeze.",
        "budget_per_day": 150,
        "attractions": [
            "Eiffel Tower",
            "Louvre Museum",
            "Notre-Dame Cathedral",
            "Arc de Triomphe",
        ],
        "safety": "Safe for tourists. Standard urban precautions apply.",
    },
    "tokyo": {
        "weather": "Cool and dry, around 16°C with clear skies.",
        "budget_per_day": 120,
        "attractions": [
            "Senso-ji Temple",
            "Tokyo Skytree",
            "Shibuya Crossing",
            "Meiji Shrine",
        ],
        "safety": "Very safe. Excellent public transportation.",
    },
    "sydney": {
        "weather": "Warm and sunny, around 24°C.",
        "budget_per_day": 140,
        "attractions": [
            "Sydney Opera House",
            "Bondi Beach",
            "Blue Mountains",
            "Taronga Zoo",
        ],
        "safety": "Safe for tourists. Standard beach safety rules apply.",
    },
}


# ============================================================================
# SPECIALIZED AGENTS
# ============================================================================


async def planning_agent(city: str, days: int) -> str:
    """
    Planning Agent: Creates detailed itineraries
    """

    @tool(approval_mode="never_require")
    def get_attractions(
        city: Annotated[str, Field(description="City name")],
    ) -> str:
        """Get top attractions for a city."""
        data = CITY_DATA.get(city.lower())
        if not data:
            return f"No data for {city}."
        attractions = ", ".join(data["attractions"])
        return f"Top attractions in {city}: {attractions}"

    @tool(approval_mode="never_require")
    def create_itinerary(
        city: Annotated[str, Field(description="Destination city")],
        days: Annotated[int, Field(description="Number of days")],
    ) -> str:
        """Create a day-by-day itinerary."""
        return (
            f"Itinerary for {city} ({days} days):\n"
            f"Day 1: Explore city center and local markets.\n"
            f"Day 2: Visit major landmarks and museums.\n"
            f"Day 3: Relax in parks and local shopping areas.\n"
            f"(Customize based on interests)"
        )

    credential = AzureCliCredential()

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=(
            "You are a travel planning expert. Create engaging itineraries "
            "that balance major attractions with local experiences."
        ),
        tools=[get_attractions, create_itinerary],
    ) as agent:
        prompt = f"Create a detailed {days}-day itinerary for {city}."
        response = await agent.run([prompt])
        return str(response)


async def budget_agent(city: str, days: int, total_budget: float) -> str:
    """
    Budget Agent: Calculates costs and provides budget breakdown
    """

    @tool(approval_mode="never_require")
    def get_daily_budget(
        city: Annotated[str, Field(description="City name")],
    ) -> str:
        """Get estimated daily budget for a city."""
        data = CITY_DATA.get(city.lower())
        if not data:
            return f"No budget data for {city}."
        daily = data["budget_per_day"]
        return f"Estimated daily budget for {city}: ${daily}"

    @tool(approval_mode="never_require")
    def calculate_total(
        daily_budget: Annotated[float, Field(description="Daily budget in USD")],
        days: Annotated[int, Field(description="Number of days")],
    ) -> str:
        """Calculate total trip cost."""
        total = daily_budget * days
        return f"Total estimated cost for {days} days: ${total}"

    credential = AzureCliCredential()

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=(
            "You are a budget analyst. Provide detailed cost breakdowns "
            "for travel. Include accommodation, food, and activities."
        ),
        tools=[get_daily_budget, calculate_total],
    ) as agent:
        prompt = f"I have ${total_budget} for a {days}-day trip to {city}. Is this enough?"
        response = await agent.run([prompt])
        return str(response)


async def weather_agent(city: str) -> str:
    """
    Weather Agent: Provides weather and packing recommendations
    """

    @tool(approval_mode="never_require")
    def get_weather(
        city: Annotated[str, Field(description="City name")],
    ) -> str:
        """Get weather forecast."""
        data = CITY_DATA.get(city.lower())
        if not data:
            return f"No weather data for {city}."
        return f"Weather in {city}: {data['weather']}"

    @tool(approval_mode="never_require")
    def packing_recommendations(
        weather: Annotated[str, Field(description="Weather description")],
    ) -> str:
        """Get packing recommendations based on weather."""
        return (
            "Packing recommendations:\n"
            "- Light, breathable clothing\n"
            "- Rain jacket or umbrella\n"
            "- Comfortable walking shoes\n"
            "- Sunscreen and hat"
        )

    credential = AzureCliCredential()

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=(
            "You are a weather expert. Provide accurate weather information "
            "and practical packing advice for travelers."
        ),
        tools=[get_weather, packing_recommendations],
    ) as agent:
        prompt = f"What's the weather in {city} and what should I pack?"
        response = await agent.run([prompt])
        return str(response)


async def safety_agent(city: str) -> str:
    """
    Safety Agent: Provides travel safety information
    """

    @tool(approval_mode="never_require")
    def get_safety_info(
        city: Annotated[str, Field(description="City name")],
    ) -> str:
        """Get safety information for a city."""
        data = CITY_DATA.get(city.lower())
        if not data:
            return f"No safety data for {city}."
        return f"Safety in {city}: {data['safety']}"

    @tool(approval_mode="never_require")
    def travel_tips(
        city: Annotated[str, Field(description="City name")],
    ) -> str:
        """Get practical travel tips."""
        return (
            "Essential travel tips:\n"
            "- Register with your embassy\n"
            "- Keep copies of important documents\n"
            "- Use registered taxis or ride-sharing\n"
            "- Stay aware of surroundings\n"
            "- Keep valuables secure"
        )

    credential = AzureCliCredential()

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=(
            "You are a travel safety expert. Provide accurate, practical "
            "safety information to help travelers prepare responsibly."
        ),
        tools=[get_safety_info, travel_tips],
    ) as agent:
        prompt = f"What should I know about safety in {city}?"
        response = await agent.run([prompt])
        return str(response)


# ============================================================================
# COORDINATOR AGENT (Orchestrates all agents)
# ============================================================================


async def coordinator_agent(city: str, days: int, budget: float) -> str:
    """
    Coordinator Agent: Orchestrates all specialized agents and synthesizes results
    """

    print("\n" + "=" * 70)
    print(f"MULTI-AGENT WORKFLOW: {city.upper()} ({days} days, ${budget} budget)")
    print("=" * 70)

    # Run all agents in parallel
    print("\n[1/5] Planning Agent - Creating itinerary...")
    planning_response = await planning_agent(city, days)
    planning_result = str(planning_response)

    print("[2/5] Budget Agent - Calculating costs...")
    budget_response = await budget_agent(city, days, budget)
    budget_result = str(budget_response)

    print("[3/5] Weather Agent - Getting weather info...")
    weather_response = await weather_agent(city)
    weather_result = str(weather_response)

    print("[4/5] Safety Agent - Getting safety information...")
    safety_response = await safety_agent(city)
    safety_result = str(safety_response)

    print("[5/5] Synthesizing results...")

    # Synthesize with coordinator
    @tool(approval_mode="never_require")
    def synthesize_results(
        planning: Annotated[str, Field(description="Itinerary from planning agent")],
        budget: Annotated[str, Field(description="Budget info from budget agent")],
        weather: Annotated[str, Field(description="Weather info from weather agent")],
        safety: Annotated[
            str, Field(description="Safety info from safety agent")
        ],
    ) -> str:
        """Combine all agent outputs into a comprehensive travel guide."""
        return (
            f"Comprehensive Travel Guide for {city}:\n\n"
            f"ITINERARY:\n{planning}\n\n"
            f"BUDGET:\n{budget}\n\n"
            f"WEATHER & PACKING:\n{weather}\n\n"
            f"SAFETY & TIPS:\n{safety}"
        )

    credential = AzureCliCredential()

    async with Agent(
        client=AzureOpenAIResponsesClient(
            credential=credential,
            deployment_name=os.getenv("MODEL_DEPLOYMENT_NAME"),
            project_endpoint=os.getenv("PROJECT_ENDPOINT"),
        ),
        instructions=(
            "You are a master travel consultant. Synthesize information from "
            "multiple specialists into a coherent, actionable travel guide."
        ),
        tools=[synthesize_results],
    ) as agent:
        prompt = (
            f"Synthesize the planning, budget, weather, and safety information "
            f"into a comprehensive guide. Planning: {planning_result[:200]}... "
            f"Budget: {budget_result[:200]}... "
            f"Weather: {weather_result[:200]}... "
            f"Safety: {safety_result[:200]}..."
        )
        response = await agent.run([prompt])
        return str(response)


# ============================================================================
# MAIN
# ============================================================================


async def main():
    import sys

    os.system("cls" if os.name == "nt" else "clear")

    print("Multi-Agent Travel Planner")
    print("==========================\n")

    # Get user input
    city = input("Which city are you visiting? ").strip()
    days_str = input("How many days is your trip? ").strip()
    budget_str = input("What's your total budget (USD)? ").strip()

    try:
        days = int(days_str)
        budget = float(budget_str)
    except ValueError:
        print("Invalid input. Please enter numbers.")
        return

    # Run multi-agent workflow
    result = await coordinator_agent(city, days, budget)

    print("\n" + "=" * 70)
    print("FINAL TRAVEL GUIDE")
    print("=" * 70)
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
