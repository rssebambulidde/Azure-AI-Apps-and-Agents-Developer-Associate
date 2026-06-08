"""
FastAPI wrapper for multi-agent travel workflow

Deploy the multi-agent system as a REST API service.
Can be deployed to Azure Functions, Azure App Service, or any cloud hosting.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import asyncio
import os
import sys

# Add parent directory to path to import multi_agent_workflow
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from multi_agent_workflow import coordinator_agent

app = FastAPI(
    title="Multi-Agent Travel Planner API",
    description="Travel planning powered by specialized AI agents",
    version="1.0.0",
)


class TravelRequest(BaseModel):
    """Travel planning request"""

    city: str
    days: int
    budget: float

    class Config:
        json_schema_extra = {
            "example": {"city": "Kampala", "days": 3, "budget": 2000}
        }


class TravelGuide(BaseModel):
    """Travel planning response"""

    city: str
    days: int
    budget: float
    guide: str


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "multi-agent-travel-planner"}


@app.post("/plan-trip", response_model=TravelGuide)
async def plan_trip(request: TravelRequest) -> TravelGuide:
    """
    Plan a trip using the multi-agent workflow.

    Args:
        request: Travel request with city, days, and budget

    Returns:
        Comprehensive travel guide synthesized by specialized agents
    """
    try:
        # Validate inputs
        if request.days < 1 or request.days > 365:
            raise ValueError("Days must be between 1 and 365")
        if request.budget < 0:
            raise ValueError("Budget must be positive")
        if not request.city or len(request.city) < 2:
            raise ValueError("City name must be at least 2 characters")

        # Run the multi-agent workflow
        guide = await coordinator_agent(request.city, request.days, request.budget)

        return TravelGuide(
            city=request.city,
            days=request.days,
            budget=request.budget,
            guide=guide,
        )

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error planning trip: {str(e)}")


@app.get("/supported-cities")
async def supported_cities():
    """Return list of cities with available data"""
    cities = {
        "kampala": {
            "country": "Uganda",
            "weather": "Tropical",
            "estimated_daily_budget_usd": 80,
        },
        "paris": {"country": "France", "weather": "Temperate", "estimated_daily_budget_usd": 150},
        "tokyo": {"country": "Japan", "weather": "Temperate", "estimated_daily_budget_usd": 120},
        "sydney": {"country": "Australia", "weather": "Subtropical", "estimated_daily_budget_usd": 140},
    }
    return cities


@app.get("/estimate-budget/{city}")
async def estimate_budget(city: str, days: int = 3):
    """Get budget estimate for a city"""
    from multi_agent_workflow import CITY_DATA

    city_lower = city.lower()
    if city_lower not in CITY_DATA:
        raise HTTPException(
            status_code=404, detail=f"No data available for {city}"
        )

    data = CITY_DATA[city_lower]
    daily_budget = data["budget_per_day"]
    total = daily_budget * days

    return {
        "city": city,
        "days": days,
        "daily_budget_usd": daily_budget,
        "total_budget_usd": total,
    }


@app.get("/")
async def root():
    """API root endpoint with documentation"""
    return {
        "service": "Multi-Agent Travel Planner API",
        "version": "1.0.0",
        "endpoints": {
            "POST /plan-trip": "Plan a complete trip (main endpoint)",
            "GET /health": "Service health check",
            "GET /supported-cities": "List available cities",
            "GET /estimate-budget/{city}": "Get budget estimate",
            "GET /docs": "Interactive API documentation (Swagger UI)",
            "GET /redoc": "Alternative API documentation (ReDoc)",
        },
        "example_request": {
            "city": "Kampala",
            "days": 3,
            "budget": 2000,
        },
    }


if __name__ == "__main__":
    import uvicorn

    # Run with: python api_wrapper.py
    # Or use: uvicorn api_wrapper:app --reload
    uvicorn.run(app, host="0.0.0.0", port=8000)
