# Integrate custom tools into your agent

## Overview
This guide explains how to add custom tools to Microsoft Foundry agents. It is written for beginners and includes step-by-step explanations, examples, tool options, best practices, and exam-ready review material.

Custom tools let an AI agent do more than generate text. They give the agent a way to call real code, access APIs, and execute reliable actions such as looking up orders, fetching records, or performing business logic.

---

## Table of Contents
1. What are custom tools?
2. Why use custom tools with agents?
3. Types of custom tools
4. How custom tools work in Foundry
5. Common custom tool examples
6. Best practices for custom tools
7. Testing and validating custom tools
8. Maintenance and security
9. Exam prep and review

---

## 1. What are custom tools?

A custom tool is a piece of code or an API that an agent can call when it needs information or needs to perform an action. Instead of relying only on the model's text generation, the agent can request the tool and receive structured results.

Examples:
- Fetch order status from a database
- Look up customer records
- Call a payment service
- Translate text using a verified API

Custom tools are especially useful when the agent needs accurate data, trusted computations, or actions that must be auditable.

---

## 2. Why use custom tools with agents?

Custom tools improve an agent in three key ways:

- **Accuracy:** The agent can use real data from trusted systems instead of guessing.
- **Reliability:** Tools return structured answers, making workflow logic more predictable.
- **Actionability:** The agent can perform real business actions, not just suggest them.

Use custom tools when your agent must do more than answer questions — when it must interact with a real system or service.

---

## 3. Types of custom tools

Microsoft Foundry supports several custom tool approaches. The most common are:

### Function calling
A lightweight way to expose a local function to the agent. The agent can invoke the function by name with typed parameters, and then the function returns structured data.

Good for:
- simple lookups
- helper operations
- quick logic inside the application

### Azure Functions
Serverless functions that run in Azure. These are great for:
- async work
- integration with other Azure services
- long-running or event-driven logic

### OpenAPI tools
Agent-accessible APIs registered with an OpenAPI specification. Use this when you have a REST or HTTP API and want the agent to call it with typed inputs and structured outputs.

Good for:
- external services
- existing APIs
- rich request/response contracts

---

## 4. How custom tools work in Foundry

### Tool registration
To use a custom tool in Foundry, you first define it in your agent configuration or tool registry.

For example:
- A Python function is wrapped as a tool with a name, description, and parameter schema.
- An Azure Function is exposed as an endpoint and registered as a tool.
- An OpenAPI tool is registered using its OpenAPI document.

### Agent decision flow
When the agent receives a prompt, it can decide whether to generate text or call a tool. If it chooses a tool, the workflow or agent service sends the tool name and parameters to your implementation.

### Tool execution
The tool runs, performs its work, and returns a result in a predictable format. The agent then uses that result to continue the conversation or complete the task.

### Structured results
Tools should return JSON-compatible data. This makes it easy for the agent and workflow to read the output and make decisions.

---

## 5. Common custom tool examples

### Example 1: Order status lookup
A retail support agent can answer questions about order delivery by calling a `get_order_status` tool.

Pseudo-code example:
```python
from azure.ai.projects import FunctionTool

def get_order_status(order_id: str) -> dict:
    # Call your order system and return JSON
    return {"order_id": order_id, "status": "Shipped", "delivery_date": "2026-06-10"}

order_tool = FunctionTool(
    name="get_order_status",
    description="Retrieve current order status by order ID.",
    func=get_order_status,
    params={"order_id": {"type": "string", "description": "The ID of the order."}}
)
```

### Example 2: Weather API via OpenAPI
Register a weather API with an OpenAPI spec so the agent can request the weather for a location.

Benefits:
- typed parameters
- documented endpoints
- stronger validation

### Example 3: Azure Function for ticket creation
If a user asks an agent to create a support ticket, the agent can call an Azure Function that writes the ticket to a queue or database.

This is useful when:
- you need serverless hosting
- you need integration with Azure services such as Storage, Service Bus, or Cosmos DB

---

## 6. Best practices for custom tools

### Define precise schemas
Provide clear parameter and response schemas so the agent knows exactly what the tool expects and returns.

### Use helpful descriptions
Write concise descriptions for tools and parameters. This helps the agent choose the right tool.

### Keep tools single-purpose
A tool should do one job well. Avoid making a single tool do too many different things.

### Secure secrets properly
Never hard-code secrets in tool code.
Use:
- Azure Key Vault
- environment variables
- managed identities
- secure worker secrets

### Log tool activity
Record tool calls and results for debugging, auditing, and monitoring.

### Fail gracefully
If a tool encounters an error, return a clear message and a status indicator. Avoid exposing internal stack traces to the agent.

### Validate inputs
Check tool inputs before calling downstream services, and return errors if the data is invalid.

---

## 7. Testing and validating custom tools

### Simple test plan
1. Add the tool to a dev version of your agent.
2. Send prompts that should trigger the tool.
3. Confirm the tool is called and returns expected data.
4. Verify the agent uses the tool output correctly.

### Unit tests
Write unit tests for your tool logic. If your tool calls an external API or database, mock those dependencies.

### End-to-end tests
Test the full agent flow, including tool invocation and result handling.

### Example exercises
- Add a `get_order_status` function tool and test it with sample prompts.
- Create an OpenAPI tool for a weather API and ask the agent for the current weather.
- Deploy an Azure Function, register it as a tool, and verify the agent can trigger it.

---

## 8. Maintenance and security

### Keep tools updated
Review tool definitions regularly and update schemas if APIs change.

### Document tool behavior
Add notes or documentation describing what each tool does, what inputs it accepts, and what output it returns.

### Monitor usage
Track which tools the agent calls most often and whether the tool outputs are successful.

### Secure access
- Use allowlists for API endpoints.
- Use private network or service endpoints when needed.
- Avoid exposing sensitive services directly to agents or external users.

---

## 9. Exam prep and review

### Key concepts to remember
- Custom tools give agents access to real code and services.
- Foundry supports function calling, Azure Functions, and OpenAPI tools.
- Tools should use typed parameters and structured results.
- Use custom tools when the agent needs accurate data or real actions.
- Secure secrets and log tool calls.

### Quick review questions
1. What is the main benefit of giving an agent a custom tool?
2. When should you choose an OpenAPI tool instead of a function tool?
3. Why is it important to return structured JSON from a tool?
4. How should you handle secrets used by custom tools?
5. What is the best way to test a custom tool?

### Model answers
1. It lets the agent perform real actions or access trusted data instead of guessing.
2. Choose OpenAPI when you already have an HTTP API or need a rich typed interface.
3. Structured JSON makes tool output predictable and easier for the agent to use.
4. Store secrets in Key Vault or secure environment variables; never hard-code them.
5. Write unit tests for tool logic and end-to-end tests for the agent flow.

### Final exam-ready summary
- Understand the different custom tool patterns.
- Know how to register and configure tools.
- Remember the importance of schema, security, and logging.
- Practice with sample tools such as order lookup, weather API, and Azure Functions.

---

## Final tips for beginners
- Start with a simple function tool before using Azure Functions or OpenAPI.
- Keep tool definitions small and focused.
- Validate input values and return clear errors.
- Test both the tool and the agent together.
- Document tool behavior so future team members understand it.

Good luck integrating custom tools into your agents!