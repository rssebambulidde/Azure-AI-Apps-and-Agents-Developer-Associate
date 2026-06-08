# Microsoft Agent Framework - Simplified for Beginners

## What is an AI Agent? (Simple Version)

An **AI agent** is a program that:
- Listens to what you ask
- Thinks about what you need
- Uses tools to get information
- Gives you an answer

**Real example you built:**
```
User: "Plan a trip to Kampala for 3 days with $2000"
     ↓
Agent thinks: "I need weather info and an itinerary"
     ↓
Agent uses tool 1: get_weather("Kampala")
Agent uses tool 2: create_itinerary("Kampala", 3)
     ↓
Agent combines: "Here's your complete travel guide..."
```

---

## Core Concepts You Already Know

### 1. **The Agent** 
The "brain" that listens and responds.

**Your code:**
```python
async with Agent(
    client=AzureOpenAIResponsesClient(...),
    instructions="You are a travel assistant",
    tools=[get_weather, create_itinerary],
) as agent:
    response = await agent.run("Plan a trip to Paris")
```

**What it does:**
- Takes your question
- Thinks about which tools to use
- Calls the tools
- Gives you the answer

---

### 2. **Tools**
Extra abilities the agent can use. Like giving the agent a toolbox.

**Two types you used:**

#### **Type 1: Local Tools (Python functions)**
```python
@tool
def get_weather(city: str) -> str:
    """Tell me the weather"""
    return weather_map[city]
```
- Runs on your computer
- Only works locally
- Portal can't use it

#### **Type 2: External Tools (HTTP/OpenAPI)**
```python
travel_tools = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="travel_tools",
        spec=openapi_spec,  # This is the "instruction manual"
    )
)
```
- Runs on a server (Cloudflare)
- Works everywhere
- Portal CAN use it

---

### 3. **Instructions**
Tells the agent what to do and how to behave.

**Your example:**
```
"You are an expert travel consultant.
 - Plan comprehensive itineraries
 - Provide realistic budgets
 - Give packing recommendations"
```

Agent reads this and acts like a travel expert.

---

## How Your Travel Agent Works (Step by Step)

```
1. USER ASKS
   "Plan a 3-day trip to Kampala with $2000"
   
2. AGENT READS INSTRUCTIONS
   "I'm a travel expert. I need weather + itinerary."
   
3. AGENT CALLS TOOLS
   Tool 1: get_weather("Kampala")
   Tool 2: create_itinerary("Kampala", 3)
   
4. AGENT GETS RESULTS
   Weather: "24°C, afternoon rain"
   Itinerary: "Day 1: Markets, Day 2: Museums, Day 3: Parks"
   
5. AGENT THINKS
   "I have the info. Now I'll create a complete guide."
   
6. AGENT RESPONDS
   "Here's your Kampala trip guide..."
```

---

## What Happens Locally vs In Portal

### **Locally (Your Computer)**
```
You run: python travel_assistant.py

What works:
✅ Local tools (@tool functions)
✅ Agent reasoning
✅ Tool calling

What doesn't:
❌ OpenAPI tools (maybe)
❌ External APIs
```

---

### **In Portal (Cloud)**
```
You go to Foundry portal

What works:
✅ External tools (OpenAPI)
✅ Agent reasoning
✅ Tool calling

What doesn't:
❌ Local Python functions
❌ Your computer's files
```

---

## The Important Rule

### **Portal agents can ONLY use external tools**

```
Local tools (@tool)
    ↓
Only work on your computer
    ↓
Portal can't see them ❌

External tools (OpenAPI)
    ↓
Work everywhere via HTTP
    ↓
Portal can use them ✅
```

---

## To Deploy Tools to Portal

### **3 Steps**

**Step 1: Create the tool endpoint**
```javascript
// cloudflare/worker/src/index.js
if (url.pathname === "/weather") {
    return new Response("Weather data here");
}
```

**Step 2: Write the instruction manual (OpenAPI spec)**
```json
// cloudflare/worker/openapi.json
{
  "paths": {
    "/weather": {
      "get": {
        "operationId": "get_weather"
      }
    }
  }
}
```

**Step 3: Tell the agent about the tool**
```python
# upgrade_agent.py
travel_tools = OpenApiTool(
    openapi=OpenApiFunctionDefinition(
        name="travel_tools",
        spec=openapi_spec,
    )
)
```

---

## When to Upgrade to Portal

### **Upgrade When:**
```
✅ You change instructions
✅ You add/change external tools
✅ You want portal to see new behavior
```

### **Don't Upgrade When:**
```
❌ Testing locally
❌ Changing local Python code
❌ Just experimenting
```

---

## Types of Agents

You've learned about different agent types:

### **1. Local Agent (Agent Framework)**
```python
# Runs only on your computer
async with Agent(tools=[...]) as agent:
    response = await agent.run(prompt)
```

### **2. Azure Foundry Agent (Enterprise)**
```python
# Runs in the cloud, accessible to anyone
with AIProjectClient(...) as client:
    agent = client.agents.create_version(...)
```

**You built BOTH!**
- Local: `travel_assistant.py`
- Cloud: `travel-assistant-demo` in portal

---

## Simple Tool Development Recipe

### **To add a new tool:**

**1. Decide: Local or External?**
```
Local only?  → Just add @tool function
For portal?  → Add to Cloudflare Worker + OpenAPI
```

**2. Write the tool**
```python
@tool
def my_tool(param: str) -> str:
    """What does this tool do?"""
    return "result"
```

**3. Describe it (so agent understands)**
```python
def my_tool(
    param: Annotated[str, Field(description="What is this?")]
) -> str:
```

**4. Add to agent**
```python
async with Agent(tools=[my_tool]) as agent:
    # Now agent can use it
```

**5. Deploy (if external)**
```bash
npm run deploy  # Update Cloudflare
python upgrade_agent.py  # Update agent
```

---

## Key Takeaways for Beginners

| Concept | Simple Explanation |
|---------|---|
| **Agent** | A program that listens, thinks, and responds |
| **Tool** | An ability the agent can use (like a skill) |
| **Local Tool** | Works on your computer only |
| **External Tool** | Works everywhere (portal too) |
| **Instructions** | How the agent should behave |
| **Deployment** | Sending your agent to the cloud |
| **Version** | A new copy of the agent with updates |

---

## What You've Mastered (Beginner to Intermediate)

✅ **Creating agents** with instructions  
✅ **Adding tools** to agents  
✅ **Understanding local vs cloud** deployment  
✅ **Upgrading agents** without creating new ones  
✅ **Tool orchestration** (agent picks right tool)  
✅ **Integration** (local + external tools)  

---

## Next Learning Steps

### **Easy (Stay at current level)**
- Add more local tools
- Improve agent instructions
- Test different prompts

### **Medium (Level up)**
- Add more external tools to Cloudflare
- Understand session management (memory)
- Build better tool descriptions

### **Advanced (Next level)**
- Multi-agent coordination
- Complex workflows
- Built-in tools (Code Interpreter, Web Search)

---

## Quick Reference

**Run locally:**
```bash
python travel_assistant.py
```

**Upgrade portal:**
```bash
python upgrade_agent.py
```

**Deploy worker changes:**
```bash
cd cloudflare/worker
npm run deploy
```

---

**That's it! You understand Microsoft Agent Framework at a beginner level.** 🎉

The concepts are simple:
1. Agent listens
2. Agent thinks
3. Agent uses tools
4. Agent responds

Everything else is just details! 🎯
