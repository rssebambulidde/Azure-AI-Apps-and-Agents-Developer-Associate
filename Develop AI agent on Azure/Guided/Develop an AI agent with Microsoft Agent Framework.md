# Microsoft Agent Framework - Comprehensive Guide for Exams

**Last Updated:** 2026-06-08  
**Difficulty Level:** Beginner to Advanced  
**Use Case:** Exam Preparation + Practical Implementation

---

## TABLE OF CONTENTS

1. [Introduction & Core Concepts](#introduction--core-concepts)
2. [Agent Framework Architecture](#agent-framework-architecture)
3. [Building Your First Agent](#building-your-first-agent)
4. [Tools & Tool Development](#tools--tool-development)
5. [Deployment Strategies](#deployment-strategies)
6. [Advanced Concepts](#advanced-concepts)
7. [Exam Preparation](#exam-preparation)
8. [Troubleshooting & Best Practices](#troubleshooting--best-practices)

---

# PART 1: INTRODUCTION & CORE CONCEPTS

## What is an AI Agent?

An **AI agent** is an intelligent program that:
- **Perceives** user input and context
- **Reasons** about what actions to take
- **Acts** by calling tools or executing functions
- **Responds** with intelligent, contextual answers

### Simple Visual

```
User Question
    ↓
Agent reads instructions (system prompt)
    ↓
Agent decides which tools to use
    ↓
Agent calls tools → Gets data
    ↓
Agent processes & synthesizes information
    ↓
Agent responds to user
```

### Real-World Example: Travel Assistant Agent

```
User: "Plan a 3-day trip to Kampala with $2000 budget"

Agent Decision Process:
1. Read instructions: "I'm a travel consultant"
2. Identify needs: weather + itinerary + budget
3. Call tools: get_weather("Kampala"), create_itinerary("Kampala", 3)
4. Synthesize: Combine weather + activities + budget advice
5. Respond: "Here's your complete Kampala guide..."
```

---

## Core Components You Need to Know

### 1. **Agent (The Brain)**
- Powered by Large Language Models (LLMs)
- Understands natural language
- Makes intelligent decisions about tool usage
- Maintains context across conversation turns

**Key Properties:**
- Instructions (system prompt)
- Tools (capabilities)
- LLM Model (reasoning engine)
- Session/Memory (conversation history)

### 2. **Tools (The Hands)**
Capabilities the agent can use to:
- Get external data
- Perform calculations
- Call APIs
- Execute functions

**Types:**
- **Local Tools**: Python functions (@tool decorator)
- **External Tools**: HTTP endpoints (OpenAPI/REST)
- **Built-in Tools**: Web search, code interpreter, etc.

### 3. **Instructions (The Rules)**
Tell the agent:
- What role to play
- How to behave
- What tone to use
- When to use tools
- Output format requirements

### 4. **Chat/Messages (The Conversation)**
- User messages
- Agent responses
- Tool calls and results
- Conversation history (context)

---

## Agent Execution Flow (Detailed)

```
Step 1: User Input
├─ User sends message: "Plan a trip"
│
Step 2: Agent Initialization
├─ Load instructions
├─ Load available tools
├─ Prepare chat history
│
Step 3: LLM Processing
├─ Send to Azure OpenAI (gpt-4)
├─ LLM analyzes: What tools do I need?
├─ LLM decides: Call get_weather + create_itinerary
│
Step 4: Tool Execution
├─ Call tool 1: get_weather("Kampala")
│   └─ Result: "24°C, afternoon rain"
├─ Call tool 2: create_itinerary("Kampala", 3)
│   └─ Result: "Day 1: Markets, Day 2: Museums..."
│
Step 5: Response Generation
├─ Send results back to LLM
├─ LLM synthesizes information
├─ Format as readable travel guide
│
Step 6: Response to User
└─ Deliver final answer with itinerary, weather, tips, etc.
```

---

# PART 2: AGENT FRAMEWORK ARCHITECTURE

## Microsoft Agent Framework Stack

```
┌─────────────────────────────────────────────┐
│        Your Application (travel_assistant.py) │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│   Microsoft Agent Framework (Python SDK)     │
│  ├─ Agent class                              │
│  ├─ Tool decorators (@tool)                  │
│  ├─ Message handling                         │
│  └─ Function calling logic                   │
└──────────────────┬──────────────────────────┘
                   │
┌──────────────────▼──────────────────────────┐
│      Azure OpenAI Response Client             │
│  ├─ LLM reasoning engine                     │
│  ├─ Tool calling capabilities                │
│  ├─ Context management                       │
│  └─ Authentication                           │
└──────────────────┬──────────────────────────┘
                   │
        ┌──────────┴──────────┐
        │                     │
    ┌───▼────┐            ┌──▼───┐
    │ Tools  │            │ LLM  │
    │ (Local)│            │(Azure)│
    └────────┘            └──────┘
```

## Key Framework Components

### **Agent Class**
```python
from agent_framework import Agent
from agent_framework.azure import AzureOpenAIResponsesClient

agent = Agent(
    client=AzureOpenAIResponsesClient(...),
    instructions="You are a travel expert",
    tools=[get_weather, create_itinerary],
    model="gpt-4",
)
```

**Responsibility:**
- Orchestrate conversation flow
- Manage tool calling
- Handle responses

### **Tools Decorator**
```python
from agent_framework import tool

@tool
def get_weather(city: str) -> str:
    """Get weather for a city"""
    return f"Weather for {city}: sunny, 24°C"
```

**How it works:**
- Decorates Python functions
- Automatically generates schemas
- Makes functions callable by agent

### **Azure OpenAI Client**
```python
from agent_framework.azure import AzureOpenAIResponsesClient

client = AzureOpenAIResponsesClient(
    credential=AzureCliCredential(),
    endpoint="https://project.services.ai.azure.com",
    model_deployment_name="gpt-4.1"
)
```

**Responsibility:**
- Connect to Azure OpenAI
- Send prompts to LLM
- Receive responses
- Handle function calling

---

## Message Types in Agent Framework

### **1. User Message**
```python
Message(
    role="user",
    content="Plan a trip to Paris for 2 days"
)
```

### **2. Assistant Message**
```python
Message(
    role="assistant",
    content="I'll help plan your Paris trip..."
)
```

### **3. Function Call**
```python
ToolCall(
    function_name="get_weather",
    arguments={"city": "Paris"}
)
```

### **4. Tool Result**
```python
ToolResult(
    tool_call_id="call_123",
    content="Weather: 18°C, partly cloudy"
)
```

---

# PART 3: BUILDING YOUR FIRST AGENT

## Step-by-Step Implementation

### **Step 1: Setup Environment**

```bash
# Create virtual environment
python -m venv .venv

# Activate (Windows)
.\.venv\Scripts\Activate.ps1

# Install dependencies
pip install azure-ai-projects azure-ai-agent-framework python-dotenv
```

### **Step 2: Configure Azure Resources**

```python
# .env file
PROJECT_ENDPOINT=https://your-project.services.ai.azure.com/api/projects/your-project
MODEL_DEPLOYMENT_NAME=gpt-4.1
```

```python
# Load environment
from dotenv import load_dotenv
import os

load_dotenv()
endpoint = os.getenv("PROJECT_ENDPOINT")
model_name = os.getenv("MODEL_DEPLOYMENT_NAME")
```

### **Step 3: Create Tools**

```python
from agent_framework import tool
from typing import Annotated
from pydantic import Field

@tool
def get_weather(
    city: Annotated[str, Field(description="City name")]
) -> str:
    """Get current weather for a city"""
    weather_data = {
        "Paris": "18°C, partly cloudy",
        "Tokyo": "16°C, rainy",
        "Sydney": "24°C, sunny",
        "Kampala": "24°C, afternoon showers"
    }
    return weather_data.get(city, "City not found")

@tool
def create_itinerary(
    city: Annotated[str, Field(description="Destination city")],
    days: Annotated[int, Field(description="Number of days")]
) -> str:
    """Create a travel itinerary"""
    itineraries = {
        "Paris": {
            1: "Day 1: Eiffel Tower, Arc de Triomphe, Seine River cruise",
            2: "Day 2: Louvre Museum, Notre-Dame, Latin Quarter",
        },
        "Tokyo": {
            1: "Day 1: Shibuya Crossing, Harajuku, Shinjuku",
            2: "Day 2: Senso-ji Temple, Asakusa, Tokyo Skytree",
        }
    }
    return itineraries.get(city, {}).get(days, "Itinerary not available")
```

### **Step 4: Create Agent**

```python
from agent_framework import Agent
from agent_framework.azure import AzureOpenAIResponsesClient
from azure.identity import AzureCliCredential

async def main():
    # Create client
    client = AzureOpenAIResponsesClient(
        credential=AzureCliCredential(),
        endpoint=endpoint,
        model_deployment_name=model_name
    )
    
    # Create agent
    async with Agent(
        client=client,
        instructions="""You are an expert travel consultant.
        - Provide comprehensive itineraries
        - Include weather and packing recommendations
        - Consider budget constraints
        - Format output clearly with sections""",
        tools=[get_weather, create_itinerary],
    ) as agent:
        # Run agent
        response = await agent.run(
            "Plan a 2-day trip to Paris with $1500 budget"
        )
        print(response)
```

### **Step 5: Run Agent Locally**

```bash
python travel_assistant.py
```

---

# PART 4: TOOLS & TOOL DEVELOPMENT

## Types of Tools

### **Type 1: Local Tools (Python Functions)**

**Definition:**
- Native Python functions decorated with `@tool`
- Execute directly on your machine
- Only work locally or in agent framework

**Pros:**
- ✅ Easy to create
- ✅ Direct access to Python libraries
- ✅ Fast execution
- ✅ Full debugging capability

**Cons:**
- ❌ Don't work in cloud/portal
- ❌ Limited to local execution
- ❌ Not accessible via HTTP

**Example:**
```python
@tool
def calculate_budget(
    hotel_cost: Annotated[float, Field(description="Daily hotel cost")],
    days: Annotated[int, Field(description="Number of days")]
) -> str:
    """Calculate trip budget"""
    total = hotel_cost * days
    return f"Total hotel cost: ${total}"
```

---

### **Type 2: External Tools (OpenAPI/HTTP)**

**Definition:**
- Tools exposed via HTTP endpoints
- Defined using OpenAPI 3.1.0 specification
- Work everywhere (local + cloud + portal)

**Pros:**
- ✅ Work in Azure Foundry portal
- ✅ Language-agnostic
- ✅ Scalable
- ✅ Can be deployed on serverless platforms

**Cons:**
- ❌ More setup required
- ❌ Network latency
- ❌ Requires specification file

**Architecture:**

```
Local Agent              Cloudflare Worker
┌──────────────┐        ┌─────────────────┐
│ Agent        │        │ HTTP Server     │
│ (Python)     │───────▶│ (JavaScript)    │
│              │        │                 │
└──────────────┘        └─────────────────┘
                        ├─ /weather
                        ├─ /itinerary
                        └─ /budget
```

**Tool Specification (OpenAPI):**

```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Travel Tools API",
    "version": "1.0.0"
  },
  "paths": {
    "/weather": {
      "get": {
        "operationId": "get_weather",
        "parameters": [
          {
            "name": "city",
            "in": "query",
            "required": true,
            "schema": {"type": "string"}
          }
        ],
        "responses": {
          "200": {
            "description": "Weather information",
            "content": {
              "application/json": {
                "schema": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}
```

**Using in Agent:**

```python
from agent_framework import OpenApiTool, OpenApiFunctionDefinition
import json

# Load OpenAPI spec
with open("openapi.json") as f:
    openapi_spec = json.load(f)

# Create tool
travel_tools = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="travel_tools",
        spec=openapi_spec,
        authentication={
            "type": "none"  # or "bearer", "api-key", etc.
        }
    )
)

# Use in agent
async with Agent(
    client=client,
    tools=[travel_tools],
) as agent:
    response = await agent.run("What's the weather in Paris?")
```

---

### **Type 3: Built-in Tools** (Advanced)

Microsoft Agent Framework provides built-in tools:
- **Web Search**: Real-time internet search
- **Code Interpreter**: Execute Python code
- **File Handling**: Read/write files

Example:
```python
from agent_framework.builtin_tools import WebSearch

agent = Agent(
    client=client,
    tools=[WebSearch()],  # Built-in tool
)
```

---

## Tool Design Best Practices

### **1. Clear Naming**
```python
# ✅ Good
@tool
def get_flight_prices(destination: str, date: str) -> str:
    pass

# ❌ Bad
@tool
def tool1(x: str, y: str) -> str:
    pass
```

### **2. Descriptive Documentation**
```python
@tool
def get_flight_prices(
    destination: Annotated[str, Field(
        description="IATA airport code (e.g., CDG for Paris)"
    )],
    date: Annotated[str, Field(
        description="Travel date in YYYY-MM-DD format"
    )]
) -> str:
    """
    Get current flight prices to a destination.
    
    Returns prices in USD for the next 30 days.
    """
    pass
```

### **3. Type Hints**
```python
# ✅ Always use type hints
@tool
def calculate_budget(amount: float, days: int) -> str:
    pass

# ❌ Avoid generic types
@tool
def calculate_budget(amount, days):
    pass
```

### **4. Error Handling**
```python
@tool
def get_weather(city: str) -> str:
    """Get weather for a city"""
    try:
        if not city:
            return "Error: City name required"
        
        weather = fetch_weather(city)
        return f"Weather for {city}: {weather}"
    except Exception as e:
        return f"Error: Could not fetch weather - {str(e)}"
```

---

# PART 5: DEPLOYMENT STRATEGIES

## Deployment Environments

### **Environment 1: Local Development**

**Command:**
```bash
python travel_assistant.py
```

**What Works:**
- ✅ Local Python tools (@tool)
- ✅ Full debugging
- ✅ Fast iteration

**What Doesn't Work:**
- ❌ External tools (sometimes)
- ❌ Portal integration

**Use When:**
- Testing new features
- Debugging issues
- Developing locally

---

### **Environment 2: Azure AI Foundry Portal**

**Access:**
- Log in to Azure AI Foundry
- Create/manage agents
- Test in chat interface
- Monitor performance

**What Works:**
- ✅ External tools (HTTP/OpenAPI)
- ✅ Scalable
- ✅ Enterprise features

**What Doesn't Work:**
- ❌ Local Python functions
- ❌ Your computer's files

**Use When:**
- Deploying to production
- Sharing with stakeholders
- Monitoring at scale

---

## Deployment Workflow

### **Workflow 1: Register Agent to Portal**

```python
# Step 1: Create agent definition
agent_definition = PromptAgentDefinition(
    name="travel-assistant-demo",
    instructions="You are a travel expert...",
    tools=[travel_tools],  # Use external tools!
)

# Step 2: Register in Foundry
with AIProjectClient(endpoint=project_endpoint, credential=credential) as client:
    agent = client.agents.create_agent(
        name="travel-assistant-demo",
        definition=agent_definition
    )
    print(f"Agent created: {agent.name} v{agent.version}")
```

**Result:**
```
✅ Agent registered in Foundry
   Name: travel-assistant-demo
   Version: 1
   Status: Ready to use in portal
```

---

### **Workflow 2: Upgrade Existing Agent (Create New Version)**

**Key Concept:**
- Same agent name
- New version number (v1 → v2 → v3 → v9)
- Automatic rollout in portal

```python
# Step 1: Update instructions or tools
new_definition = PromptAgentDefinition(
    name="travel-assistant-demo",
    instructions="Enhanced instructions here...",
    tools=[updated_tools],
)

# Step 2: Create new version
with AIProjectClient(endpoint=project_endpoint, credential=credential) as client:
    new_version = client.agents.create_version(
        agent_name="travel-assistant-demo",
        definition=new_definition
    )
    print(f"New version created: v{new_version.version}")
```

**Why This Approach:**
- ✅ No duplicate agents
- ✅ Easy rollback (use old version)
- ✅ Version history maintained
- ✅ Portal auto-uses latest

---

### **Workflow 3: Deploy External Tools**

**The 3-Step Process:**

```
Step 1: Deploy Tool Server
├─ Create HTTP endpoints
├─ Deploy to Cloudflare/Azure Functions
└─ Test endpoints

Step 2: Create OpenAPI Specification
├─ Document tool interfaces
├─ Define parameters & responses
└─ Validate against spec

Step 3: Register Tools with Agent
├─ Load OpenAPI spec
├─ Create OpenApiTool
├─ Attach to agent
└─ Upgrade agent in portal
```

**Detailed Example:**

**Step 1: Deploy Server (Cloudflare Worker)**
```javascript
// cloudflare/worker/src/index.js
export default {
  async fetch(request) {
    const url = new URL(request.url);
    
    if (url.pathname === "/weather") {
      const city = url.searchParams.get("city");
      return new Response(`Weather for ${city}: 24°C, sunny`);
    }
    
    if (url.pathname === "/itinerary") {
      const city = url.searchParams.get("city");
      const days = url.searchParams.get("days");
      return new Response(`${days}-day itinerary for ${city}...`);
    }
    
    return new Response("Not found", { status: 404 });
  }
};
```

**Deploy:**
```bash
npm run deploy
# Result: https://your-worker.workers.dev
```

---

**Step 2: Create OpenAPI Spec**
```json
{
  "openapi": "3.1.0",
  "info": {
    "title": "Travel Tools",
    "version": "1.0.0"
  },
  "servers": [
    {
      "url": "https://your-worker.workers.dev"
    }
  ],
  "paths": {
    "/weather": {
      "get": {
        "operationId": "get_weather",
        "parameters": [
          {
            "name": "city",
            "in": "query",
            "required": true,
            "schema": {"type": "string"}
          }
        ],
        "responses": {
          "200": {
            "description": "Weather data",
            "content": {
              "application/json": {
                "schema": {"type": "string"}
              }
            }
          }
        }
      }
    }
  }
}
```

---

**Step 3: Register with Agent**
```python
# Load spec
with open("openapi.json") as f:
    spec = json.load(f)

# Create tool
tool = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="travel_tools",
        spec=spec
    )
)

# Upgrade agent
definition = PromptAgentDefinition(
    name="travel-assistant-demo",
    instructions="You are a travel expert...",
    tools=[tool]
)

# Create new version
with AIProjectClient(...) as client:
    client.agents.create_version(
        agent_name="travel-assistant-demo",
        definition=definition
    )
```

---

# PART 6: ADVANCED CONCEPTS

## Session Management & Conversation Context

### **What is a Session?**
A session maintains conversation history for multi-turn interactions.

```python
# Create session
from agent_framework import AgentSession

session = AgentSession()

# Multiple turns
response1 = await agent.run("What's the weather?", session=session)
response2 = await agent.run("For how many days?", session=session)
# Agent remembers the context from turn 1
```

---

## Multi-Agent Workflows

### **Pattern 1: Sequential Workflow**
```
User Question
    ↓
Agent 1 (Planner) → Plan trip structure
    ↓
Agent 2 (Budget) → Calculate costs
    ↓
Agent 3 (Weather) → Get weather info
    ↓
Coordinator Agent → Synthesize all info
    ↓
Final Response
```

### **Pattern 2: Parallel Workflow**
```
User Question
    ↓
    ├─→ Agent 1 (get weather)
    ├─→ Agent 2 (get itinerary)
    ├─→ Agent 3 (get budget)
    └─→ Agent 4 (get safety info)
    ↓
Coordinator waits for all agents
    ↓
Synthesize results
    ↓
Final Response
```

**Implementation:**
```python
import asyncio

async def run_parallel_agents(query):
    # Run agents concurrently
    weather_task = weather_agent.run(query)
    itinerary_task = itinerary_agent.run(query)
    budget_task = budget_agent.run(query)
    
    # Wait for all
    results = await asyncio.gather(
        weather_task,
        itinerary_task,
        budget_task
    )
    
    # Combine results
    return coordinator.synthesize(results)
```

---

## Tool Calling Mechanics

### **How Agent Framework Decides to Call Tools**

```
1. User sends: "Plan a trip to Paris"
        ↓
2. Agent reads instructions
        ↓
3. Agent sees available tools:
   - get_weather(city)
   - create_itinerary(city, days)
        ↓
4. Agent's LLM decides:
   "I need weather + itinerary, so I'll call both tools"
        ↓
5. Framework generates tool calls:
   [
     ToolCall(function="get_weather", args={"city": "Paris"}),
     ToolCall(function="create_itinerary", args={"city": "Paris", "days": 3})
   ]
        ↓
6. Framework executes both tools
        ↓
7. Framework collects results and sends back to LLM
        ↓
8. LLM synthesizes and responds to user
```

### **Controlling Tool Calls with Instructions**

```python
instructions = """
You are a travel consultant.

IMPORTANT RULES:
1. ALWAYS call get_weather first before suggesting activities
2. ALWAYS provide budget estimates
3. ONLY suggest activities that match the weather
4. Use all available tools to create comprehensive plans

When a user asks for a trip:
- Use get_weather to understand conditions
- Use create_itinerary for day-by-day plans
- Synthesize both to create expert recommendations
"""
```

---

## Error Handling & Retry Logic

```python
@tool
def get_weather(city: str) -> str:
    """Get weather with error handling"""
    max_retries = 3
    retry_count = 0
    
    while retry_count < max_retries:
        try:
            response = requests.get(f"https://api.weather.com/{city}")
            if response.status_code == 200:
                return response.text
            else:
                retry_count += 1
                time.sleep(1)  # Wait before retry
        except requests.RequestException:
            retry_count += 1
            time.sleep(1)
    
    return f"Failed to get weather for {city} after {max_retries} attempts"
```

---

# PART 7: EXAM PREPARATION

## Key Concepts to Remember

### **1. Agent Components**
```
AGENT = Instructions + Tools + LLM Client + Message Handler

Instructions: How agent should behave
Tools: What agent can do
LLM Client: Reasoning engine (Azure OpenAI)
Message Handler: Conversation management
```

### **2. Tool Types**
```
Local Tools:      @tool functions, Python-only
External Tools:   HTTP endpoints, HTTP/OpenAPI, works everywhere
Built-in Tools:   Code Interpreter, Web Search
```

### **3. Local vs Portal**
```
Local:            Python code, @tool functions, local execution
Portal:           External tools, HTTP endpoints, scalable
```

### **4. Deployment Process**
```
1. Create agent definition
2. Register in Foundry
3. Test in portal
4. Create versions to upgrade
```

---

## Exam-Style Questions & Answers

### **Question 1: What is the difference between local tools and external tools?**

**Answer:**
Local tools are Python functions decorated with @tool that run on your machine. External tools are HTTP endpoints defined with OpenAPI specs that work everywhere. Portals can only use external tools.

---

### **Question 2: How do you update an agent without creating a new one?**

**Answer:**
Use the create_version() method on the existing agent. This increments the version number (v1 → v2) but keeps the same agent name. The portal automatically uses the latest version.

```python
client.agents.create_version(
    agent_name="travel-assistant-demo",
    definition=new_definition
)
```

---

### **Question 3: What is an OpenAPI specification?**

**Answer:**
An OpenAPI 3.1.0 JSON file that documents HTTP endpoints in a standard format. It defines:
- What endpoints exist
- What parameters they accept
- What responses they return
- Authentication requirements

It's like an instruction manual for tools.

---

### **Question 4: Explain the tool calling process.**

**Answer:**
1. User sends message to agent
2. Agent reads its instructions and sees available tools
3. Agent's LLM decides which tools are needed
4. Framework generates ToolCall objects
5. Framework executes the tools
6. Framework collects results
7. LLM synthesizes results and responds to user

---

### **Question 5: When should you use multi-agent workflows?**

**Answer:**
When you have complex problems that benefit from specialized agents:
- Sequential workflows: Each agent builds on previous
- Parallel workflows: Multiple agents work simultaneously
- Coordinator pattern: Specialist agents + coordinator that synthesizes

Example: Travel planning (Planner → Budget → Weather → Safety → Coordinator)

---

## Important Code Patterns

### **Pattern 1: Basic Agent Creation**
```python
async with Agent(
    client=client,
    instructions="Your role here",
    tools=[tool1, tool2],
) as agent:
    response = await agent.run("User query")
```

### **Pattern 2: Tool with Proper Annotations**
```python
@tool
def my_tool(
    param1: Annotated[str, Field(description="What is this?")],
    param2: Annotated[int, Field(description="What is this?")]
) -> str:
    """One-line description of what this tool does"""
    return "result"
```

### **Pattern 3: External Tool Setup**
```python
with open("openapi.json") as f:
    spec = json.load(f)

tool = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="tool_name",
        spec=spec
    )
)
```

### **Pattern 4: Upgrade Agent**
```python
definition = PromptAgentDefinition(
    name="agent_name",
    instructions="Updated instructions",
    tools=[tools]
)

with AIProjectClient(...) as client:
    client.agents.create_version(
        agent_name="agent_name",
        definition=definition
    )
```

---

# PART 8: TROUBLESHOOTING & BEST PRACTICES

## Common Issues & Solutions

### **Issue 1: Portal Shows "No tools available"**

**Cause:** Using local @tool functions in portal

**Solution:**
```python
# ❌ Wrong - Portal can't see local functions
@tool
def local_function():
    pass

agent = Agent(tools=[local_function])  # Won't work in portal

# ✅ Right - Use external tools
tool = OpenApiTool(spec=openapi_spec)
agent = Agent(tools=[tool])  # Works in portal
```

---

### **Issue 2: Agent not calling tools**

**Cause:** Instructions don't mention tools, or tool descriptions are unclear

**Solution:**
```python
# ✅ Good instructions
instructions = """
You are a travel expert.

REQUIRED: You MUST use the get_weather tool before recommending activities.
REQUIRED: You MUST use create_itinerary for every trip plan.

Format your response as:
- ITINERARY: [from tool]
- WEATHER: [from tool]
- TIPS: [your expertise]
"""
```

---

### **Issue 3: Tool returns wrong format**

**Cause:** Tool not returning expected data type

**Solution:**
```python
# ❌ Bad - ambiguous format
@tool
def get_data() -> str:
    data = {"key": "value"}
    return data  # Wrong! Should be string

# ✅ Good - explicit formatting
@tool
def get_data() -> str:
    data = {"key": "value"}
    return json.dumps(data)  # Always string
```

---

### **Issue 4: Tool calling fails in portal**

**Cause:** Endpoint not accessible, wrong URL in OpenAPI spec

**Solution:**
```python
# Test the endpoint manually
curl https://your-worker.workers.dev/weather?city=Paris

# If fails with 403, add User-Agent header
curl -H "User-Agent: Mozilla/5.0" https://your-worker.workers.dev/weather?city=Paris
```

---

## Best Practices

### **1. Always Include Tool Descriptions**
```python
# ✅ Good
@tool
def get_weather(
    city: Annotated[str, Field(description="City name (e.g., Paris, Tokyo)")]
) -> str:
    """Get current weather and temperature for a city"""
    pass

# ❌ Bad
@tool
def get_weather(city: str) -> str:
    pass
```

### **2. Write Clear Instructions**
```python
instructions = """
# Role
You are an expert travel consultant with 10 years of experience.

# Capabilities
You can use these tools:
- get_weather: Get current weather
- create_itinerary: Plan daily activities

# Rules
1. ALWAYS check weather before suggesting outdoor activities
2. ALWAYS provide budget estimates
3. Format output with clear sections

# Output Format
[ITINERARY]
[WEATHER]
[BUDGET]
[TIPS]
[SAFETY]
"""
```

### **3. Version Everything**
```python
# ✅ Good - track versions
# v1: Initial agent
# v2: Added budget tool
# v3: Improved instructions
# v4: Fixed tool descriptions
# v5: Added safety recommendations

client.agents.create_version(...)
```

### **4. Test Locally First**
```python
# Test with local tools
@tool
def my_tool(...):
    pass

# Run locally
python agent.py

# Once tested, convert to external tool
# Deploy to Cloudflare
# Create OpenAPI spec
# Upgrade agent in portal
```

### **5. Monitor Tool Performance**
```python
@tool
def monitored_tool(param: str) -> str:
    """Tool with monitoring"""
    import time
    start = time.time()
    
    try:
        result = expensive_operation(param)
        duration = time.time() - start
        print(f"Tool executed in {duration}s")
        return result
    except Exception as e:
        print(f"Tool failed: {str(e)}")
        return f"Error: {str(e)}"
```

---

## Exam Checklist

Before your exam, ensure you understand:

- [ ] **Architecture**: How Agent Framework components work together
- [ ] **Tools**: Local vs External, when to use each
- [ ] **Deployment**: Local → Portal workflow
- [ ] **Versioning**: Why use create_version() instead of new agent
- [ ] **Instructions**: How to write effective system prompts
- [ ] **Tool Calling**: How agents decide which tools to use
- [ ] **OpenAPI**: Structure and purpose
- [ ] **Troubleshooting**: Common issues and solutions
- [ ] **Best Practices**: Design patterns and code quality
- [ ] **Real Example**: Your travel assistant implementation

---

## Quick Reference Card

```
╔══════════════════════════════════════════════════════════════╗
║           MICROSOFT AGENT FRAMEWORK - QUICK REF              ║
╠══════════════════════════════════════════════════════════════╣
║ BASIC STRUCTURE                                              ║
║  Agent = Client + Instructions + Tools + Messages            ║
║                                                              ║
║ TOOL TYPES                                                   ║
║  Local:    @tool decorator, Python functions                ║
║  External: HTTP endpoints, OpenAPI spec, works everywhere    ║
║                                                              ║
║ KEY CLASSES                                                  ║
║  Agent: Main orchestrator                                   ║
║  AzureOpenAIResponsesClient: LLM connection                  ║
║  OpenApiTool: External tool wrapper                          ║
║                                                              ║
║ DEPLOYMENT                                                   ║
║  Local: python script.py                                    ║
║  Cloud: create_version() in Foundry                          ║
║                                                              ║
║ TOOL DEVELOPMENT                                             ║
║  1. Create tool (function or endpoint)                       ║
║  2. Document (annotations, descriptions)                     ║
║  3. Add to agent (tools=[...])                               ║
║  4. Test locally                                             ║
║  5. Deploy externally                                        ║
║  6. Upgrade agent version                                    ║
║                                                              ║
║ INSTRUCTIONS FORMULA                                         ║
║  Role + Context + Constraints + Output Format                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
```

---

## Additional Resources

**Official Documentation:**
- [Microsoft Agent Framework Docs](https://microsoft.com/en-us/agent-framework)
- [Azure AI Foundry Portal](https://foundry.microsoft.com)
- [OpenAPI 3.1.0 Spec](https://spec.openapis.org/oas/v3.1.0)

**Learning Path:**
1. Start: This guide (fundamentals)
2. Practice: Build local agents with @tool functions
3. Advance: Deploy external tools and test in portal
4. Master: Multi-agent workflows and advanced patterns

---

## Study Tips for Exams

1. **Understand the Flow**: Spend time on the execution flow diagrams
2. **Practice Coding**: Write agents, tools, and OpenAPI specs
3. **Know Your Components**: Memorize Agent, Tool, Instructions, Client
4. **Test Yourself**: Answer the exam-style questions
5. **Build Projects**: Your travel assistant is a perfect learning project
6. **Review Patterns**: Study the code patterns section repeatedly
7. **Real-World Context**: Think about how concepts apply to real agents

---

**Last Updated:** June 8, 2026  
**Status:** Comprehensive Exam Study Guide ✅  
**Ready to Study?** Start with Part 1 and work your way through!

