# Multi-Agent Workflow Guide

## Architecture

```
User Input (city, days, budget)
         ↓
   Coordinator Agent
    ↙   ↓   ↓   ↘
Planning Budget Weather Safety
Agent    Agent  Agent    Agent
 ↓        ↓      ↓        ↓
[Local Tools & LLM Reasoning]
 ↑        ↑      ↑        ↑
[Specialized Knowledge & Skills]
 ↓        ↓      ↓        ↓
Results  Results Results Results
 ↖   ↙   ↓   ↘  ↗
   Coordinator Synthesizes
         ↓
   Final Travel Guide
```

## Key Concepts

### 1. **Specialized Agents**
Each agent has:
- **Domain expertise** (travel planning, budgeting, weather, safety)
- **Specific tools** (itinerary builder, budget calculator, etc.)
- **Clear instructions** (role definition)

### 2. **Parallel Execution**
All agents run simultaneously:
```python
planning_result = await planning_agent(city, days)
budget_result = await budget_agent(city, days, budget)
weather_result = await weather_agent(city)
safety_result = await safety_agent(city)
# All 4 run in parallel, then coordinator synthesizes
```

### 3. **Tool-Based Reasoning**
Each agent has tools:
- `planning_agent`: `get_attractions()`, `create_itinerary()`
- `budget_agent`: `get_daily_budget()`, `calculate_total()`
- `weather_agent`: `get_weather()`, `packing_recommendations()`
- `safety_agent`: `get_safety_info()`, `travel_tips()`

### 4. **Coordinator Pattern**
The coordinator:
- Receives outputs from all agents
- Uses a tool to synthesize results
- Produces a cohesive final output

---

## How to Extend It

### Option 1: Add a New Specialist Agent

Example: **Restaurant Agent** (recommends dining)

```python
async def restaurant_agent(city: str) -> str:
    """Restaurant recommender"""
    
    @tool(approval_mode="never_require")
    def get_restaurants(city: Annotated[str, Field(description="City name")]) -> str:
        """Get top restaurants."""
        return f"Top restaurants in {city}:..."
    
    @tool(approval_mode="never_require")
    def get_cuisine_by_budget(budget: Annotated[float, Field(description="Budget per meal")]) -> str:
        """Recommend cuisine based on budget."""
        return "For $20/meal, try local restaurants..."
    
    credential = AzureCliCredential()
    async with Agent(
        client=AzureOpenAIResponsesClient(...),
        instructions="You are a restaurant expert. Recommend dining experiences.",
        tools=[get_restaurants, get_cuisine_by_budget],
    ) as agent:
        prompt = f"What are the best restaurants in {city}?"
        response = await agent.run([prompt])
        return str(response)
```

Then add to coordinator:
```python
# In coordinator_agent():
print("[5/6] Restaurant Agent - Finding dining recommendations...")
restaurant_result = await restaurant_agent(city)

# Update synthesize_results tool to include restaurant data
```

### Option 2: Add Dynamic Data Sources

Currently using static `CITY_DATA`. Upgrade to:

```python
# Use OpenWeatherMap API
async def get_real_weather(city: str) -> str:
    """Fetch live weather data"""
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            data = await resp.json()
            return f"Temp: {data['main']['temp']}°C, {data['weather'][0]['description']}"

# Use Booking.com API
async def get_hotel_prices(city: str) -> str:
    """Fetch real hotel prices"""
    ...

# Use a travel database
async def get_attractions_from_db(city: str) -> str:
    """Query attractions database"""
    ...
```

### Option 3: Create Agent Workflows

Chain agents together (one agent's output → next agent's input):

```python
async def planning_with_budget_constraints(city: str, days: int, budget: float) -> str:
    """Planning agent that considers budget constraints"""
    
    # Step 1: Budget agent determines daily spend
    budget_info = await budget_agent(city, days, budget)
    
    # Step 2: Planning agent uses budget_info to suggest appropriate activities
    @tool(approval_mode="never_require")
    def create_itinerary_within_budget(budget_summary: str) -> str:
        """Create itinerary that respects budget limits"""
        return f"Based on ${budget/days}/day budget, here's what to do..."
    
    # Run with budget context
    ...
```

### Option 4: Add Sub-Agents

Create hierarchical agents:

```python
async def activity_coordinator_agent(city: str) -> str:
    """Coordinates multiple activity sub-agents"""
    
    outdoor_result = await outdoor_activities_agent(city)
    cultural_result = await cultural_activities_agent(city)
    nightlife_result = await nightlife_agent(city)
    
    # Synthesize into activity recommendations
    ...
```

---

## Testing & Validation

### Test Locally
```bash
cd travel_assistant_demo
python multi_agent_workflow.py
# Input: Kampala, 5, 3000
```

### Test Different Scenarios
```python
# Low budget scenario
await coordinator_agent("Paris", 2, 500)  # $500 for 2 days

# Long trip
await coordinator_agent("Tokyo", 10, 5000)  # $5000 for 10 days

# New destination (add to CITY_DATA first)
await coordinator_agent("NewYork", 3, 4000)
```

### Performance Monitoring
```python
import time

start = time.time()
result = await coordinator_agent(city, days, budget)
elapsed = time.time() - start

print(f"Execution time: {elapsed:.2f} seconds")
# Parallel execution should be ~N+1 seconds (where N = slowest agent)
```

---

## Deploy to Foundry

Once ready:

1. **Create a Foundry agent** with the workflow:
```python
def register_foundry_workflow():
    project_client = AIProjectClient(...)
    
    # Define tool that calls coordinator_agent
    workflow_definition = PromptAgentDefinition(
        model="gpt-4",
        instructions="Provide comprehensive travel planning using specialized agents.",
        tools=[...]  # If you want to expose coordinator as an API
    )
    
    agent = project_client.agents.create_version(
        agent_name="multi-agent-travel-planner",
        definition=workflow_definition,
    )
```

2. **Test in portal** with queries like:
   - "Plan a 5-day trip to Paris with $2000"
   - "I'm going to Tokyo for 10 days. What should I budget?"

3. **Monitor** conversation traces to see multi-agent execution flow

---

## Next Steps

Pick one and we'll implement it:

1. ✅ **Add Restaurant Agent** (quick, shows extension pattern)
2. 🔄 **Integrate Real APIs** (weather, hotels, attractions)
3. 🎯 **Create Agent Workflows** (sequential execution, dependencies)
4. 🚀 **Deploy to Foundry Portal** (production-ready)
5. 📊 **Add Evaluation Dataset** (measure quality, optimize prompts)

Which interests you most?
