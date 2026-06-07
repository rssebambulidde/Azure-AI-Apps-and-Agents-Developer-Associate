# Integrate custom tools into your agent

Short, practical guide to extending a Foundry agent with custom tools.

Learning objectives
- Explain why custom tools are useful.
- Compare function calling, Azure Functions, and OpenAPI tools.
- Add a simple custom tool to a Foundry agent and test it.

Prerequisites
- Basic Azure knowledge and access to a Foundry project.
- Familiarity with Python or another server language.

Overview — what custom tools do
- Give agents code-level access to systems (databases, APIs, business logic).
- Let agents perform reliable, auditable actions (create tickets, fetch records, call back-end services).

Main options (short)
- Function calling: Define lightweight functions the agent can invoke directly. Good for inline logic and small helpers.
- Azure Functions: Serverless endpoints for async or long-running tasks; integrates well with queues and bindings.
- OpenAPI tools: Register an API with an OpenAPI spec so the agent can call any HTTP service with typed parameters.

Quick example (function calling)
```
def get_order_status(order_id: str) -> dict:
	# call internal service, return JSON
	return {"order_id": order_id, "status": "Shipped"}
```
Register this as a FunctionTool (name, parameters, description) so the agent can call it by name.

Best practices
- Define precise parameter schemas and helpful descriptions.
- Never embed secrets in client code; use secrets storage (Key Vault, Worker secrets).
- Log tool calls and results for audit and debugging.
- Fail safely: return clear errors the agent can surface to users.

Simple test plan
1. Add the tool to a dev agent and run sample prompts that should trigger it.
2. Verify tool output, logs, and that the agent uses the tool correctly.
3. Add unit tests for the tool logic and an end-to-end test for the agent workflow.

Exercises
- Add a `get_order_status` function tool to your agent and test it with example prompts.
- Create an OpenAPI spec for a simple weather API and register it as an OpenAPI tool.
- Deploy an Azure Function to handle a queue-triggered task and wire it into the agent.

Next steps
- Secure secrets and restrict direct access to back-end services (allowlist Cloudflare or use private endpoints).
- Add monitoring and budgets for resources used by custom tools.

References
- Function calling, Azure Functions, and OpenAPI tooling are supported by Foundry agent definitions and the Azure SDK.

## Learning objectives
By the end of this module, you'll be able to:

- Describe the benefits of using custom tools with your agent.
- Explore the different options for custom tools.
- Build an agent that integrates custom tools using the Microsoft Foundry Agent Service.

## Prerequisites

- Familiarity with Azure and the Azure portal.
- An understanding of generative AI. You can learn more with [Fundamentals of Generative AI](https://learn.microsoft.com/en-us/training/modules/fundamentals-generative-ai/).
- It's highly recommended you have experience with the Microsoft Foundry Agent Service. You can learn more with [Develop an AI agent with Microsoft Foundry Agent Service](https://learn.microsoft.com/en-us/training/modules/develop-ai-agent-azure/).

## This module is part of these learning paths

- [Develop AI agents on Azure](https://learn.microsoft.com/training/paths/develop-ai-agents-azure/)

- [Introduction](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/1-introduction)2 min
- [Why use custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/2-why-use-custom-tools)3 min
- [Options for implementing custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/3-custom-tool-options)6 min
- [How to integrate custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/4-how-use-custom-tools)7 min
- [Exercise - Build an agent with custom tools](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/5-exercise)30 min
- [Module assessment](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/6-knowledge-check)3 min
- [Summary](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/7-summary)2 min

---

## Module assessment
Assess your understanding of this module. Sign in and answer all questions correctly to earn a pass designation on your profile.

[](https://learn.microsoft.com/training/modules/build-agent-with-custom-tools/6-knowledge-check/).# Introduction
100 XP

- 2 minutes

Choose your preferred content format
Microsoft Foundry Agent Service offers a seamless way to build an agent without needing extensive AI or machine learning expertise. By using tools, you can provide your agent with functionality to execute actions on your behalf.

The AI Agent Service provides built-in tools for gathering knowledge and generating code, which provide your agent with some powerful functionality. However, sometimes your agent needs to be able to complete specific tasks or actions that an AI model would struggle to handle on its own. To accomplish these actions, you can provide your agent a *custom tool* based on your own code or a third-party service or API.

Imagine you're working in the retail industry, and your company is struggling with managing customer inquiries efficiently. The customer support team is overwhelmed with repetitive questions, leading to delays in response times and decreased customer satisfaction. By using Foundry Agent Service with custom tools, you can create a custom FAQ agent that handles common inquiries. This agent can be provided with a set of custom tools to look up customer orders, freeing up your support team to focus on more complex issues.

In this module, you'll learn how to utilize custom tools in Foundry Agent Service to enhance productivity, improve accuracy, and create tailored solutions for specific needs.

---

## Next unit: Why use custom tools
[](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/2-why-use-custom-tools/)

Need help? See our [troubleshooting guide](https://learn.microsoft.com/en-us/training/support/troubleshooting?uid=learn.wwl.build-agent-with-custom-tools.introduction&documentId=91d1c99b-790b-cb0c-55f0-807b366a16a7&versionIndependentDocumentId=d168e7ec-8947-8dd8-ef03-5b60ad919ab6&platformId=d9e6063e-8555-505e-ad64-b6e0d6494949&contentPath=%2FMicrosoftDocs%2Flearn-pr%2Fblob%2Flive%2Flearn-pr%2Fwwl-data-ai%2Fbuild-agent-with-custom-tools%2F1-introduction.yml&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Ftraining%2Fmodules%2Fbuild-agent-with-custom-tools%2F1-introduction%3Fpivots%3Dtext&author=berryivor) or provide specific feedback by [reporting an issue](https://learn.microsoft.com/en-us/training/support/troubleshooting?uid=learn.wwl.build-agent-with-custom-tools.introduction&documentId=91d1c99b-790b-cb0c-55f0-807b366a16a7&versionIndependentDocumentId=d168e7ec-8947-8dd8-ef03-5b60ad919ab6&platformId=d9e6063e-8555-505e-ad64-b6e0d6494949&contentPath=%2FMicrosoftDocs%2Flearn-pr%2Fblob%2Flive%2Flearn-pr%2Fwwl-data-ai%2Fbuild-agent-with-custom-tools%2F1-introduction.yml&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Ftraining%2Fmodules%2Fbuild-agent-with-custom-tools%2F1-introduction%3Fpivots%3Dtext&author=berryivor)# Why use custom tools
100 XP

- 3 minutes

Choose your preferred content format
Microsoft Foundry Agent Service offers a powerful platform for integrating custom tools to enhance productivity and provide tailored solutions for specific business needs. By using these custom tools, businesses can achieve greater efficiency and effectiveness in their operations.

## Why use custom tools?
Custom tools significantly enhance productivity by automating repetitive tasks and streamlining workflows that are specific to your use case. These tools improve accuracy by providing precise and consistent outputs, reducing the likelihood of human error. Additionally, custom tools offer tailored solutions that address specific business needs, enabling organizations to optimize their processes and achieve better outcomes.

- **Enhanced productivity**: Automate repetitive tasks and streamline workflows.
- **Improved accuracy**: Provide precise and consistent outputs, reducing human error.
- **Tailored solutions**: Address specific business needs and optimize processes.

Adding tools makes custom functionality available for the agent to use, depending on how it decides to respond to the user prompt. For example, consider how a custom tool to retrieve weather data from an external meteorological service could be used by an agent.

![Diagram showing an agent using a custom tool t call an external meteorological service.](https://learn.microsoft.com/en-us/training/wwl-data-ai/build-agent-with-custom-tools/media/agent-tool-diagram.png)

The diagram shows the process of an agent choosing to use the custom tool:

1. A user asks an agent about the weather conditions in a ski resort.
2. The agent determines that it has access to a tool that can use an API to get meteorological information, and calls it.
3. The tool returns the weather report, and the agent informs the user.

## Common scenarios for custom tools in agents
Custom tools within the Foundry Agent Service enable users to extend the capabilities of AI agents, tailoring them to meet specific business needs. Some example use cases that illustrate the versatility and impact of custom tools include:

### Customer support automation

- **Scenario**: A retail company integrates a custom tool that connects the Azure AI Agent to their customer relationship management (CRM) system.
- **Functionality**: The AI agent can retrieve customer order histories, process refunds, and provide real-time updates on shipping statuses.
- **Outcome**: Faster resolution of customer queries, reduced workload for support teams, and improved customer satisfaction.

### Inventory management

- **Scenario**: A manufacturing company develops a custom tool to link the AI agent with their inventory management system.
- **Functionality**: The AI agent can check stock levels, predict restocking needs using historical data, and place orders with suppliers automatically.
- **Outcome**: Streamlined inventory processes and optimized supply chain operations.

### Healthcare appointment scheduling

- **Scenario**: A healthcare provider integrates a custom scheduling tool with the AI agent.
- **Functionality**: The AI agent can access patient records, suggest available appointment slots, and send reminders to patients.
- **Outcome**: Reduced administrative burden, improved patient experience, and better resource utilization.

### IT Helpdesk support

- **Scenario**: An IT department develops a custom tool to integrate the AI agent with their ticketing and knowledge base systems.
- **Functionality**: The AI agent can troubleshoot common technical issues, escalate complex problems, and track ticket statuses.
- **Outcome**: Faster issue resolution, reduced downtime, and improved employee productivity.

### E-learning and training

- **Scenario**: An educational institution creates a custom tool to connect the AI agent with their learning management system (LMS).
- **Functionality**: The AI agent can recommend courses, track student progress, and answer questions about course content.
- **Outcome**: Enhanced learning experiences, increased student engagement, and streamlined administrative tasks.

These examples demonstrate how custom tools within the Foundry Agent Service can be used across industries to address unique challenges, drive efficiency, and deliver value.

---

## Next unit: Options for implementing custom tools
[](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/1-introduction/)[](https://learn.microsoft.com/en-us/training/modules/build-agent-with-custom-tools/3-custom-tool-options/)

Need help? See our [troubleshooting guide](https://learn.microsoft.com/en-us/training/support/troubleshooting?uid=learn.wwl.build-agent-with-custom-tools.why-use-custom-tools&documentId=2a6ac97d-2097-465b-0a3b-b400e356cab9&versionIndependentDocumentId=0f6c124f-13f6-d511-d668-13106c462437&platformId=16354dd7-a46a-cdd2-f047-07e05c59e4b3&contentPath=%2FMicrosoftDocs%2Flearn-pr%2Fblob%2Flive%2Flearn-pr%2Fwwl-data-ai%2Fbuild-agent-with-custom-tools%2F2-why-use-custom-tools.yml&url=https%3A%2F%2Flearn.microsoft.com%2Fen-us%2Ftraining%2Fmodules%2Fbuild-agent-with-custom-tools%2F2-why-use-custom-tools%3Fpivots%3Dtext&author=berryivor) or provide specific feedback by [reporting an issue](https://learn.microsoft.com/en-us/training/support/troubleshooting?uid=learn.wwl.build-agent-with-custom-tools.why-use-custom-tools&documentId=2a6ac97d-2097-465b-0a3b-b400e356cab9&versionIndependentDocumentId=0f6c124f-13f6-d511-d668-13106c462437&platformId=16354dd7-a46a-cdd2-f047-07e05c59e4b3&contentPath=%2FMicrosoftDocs%2Flearn-pr%2Fblob%2Flive%2Flearn-pr%2Fwwl-data-ai%2Fbuild-agent-with-custom-tools%2F2-why-use-custom-tools%3Fpivots%3Dtext&author=berryivor)# How to integrate custom tools
100 XP

- 7 minutes

Choose your preferred content format
Custom tools in an agent can be defined in a handful of ways, depending on what works best for your scenario. You may find that your company already has Azure Functions implemented for your agent to use, or a public OpenAPI specification gives your agent the functionality you're looking for.

## Function Calling
Function calling allows agents to execute predefined functions dynamically based on user input. This feature is ideal for scenarios where agents need to perform specific tasks, such as retrieving data or processing user queries, and can be done in code from within the agent. Your function may call out to other APIs to get additional information or initiate a program.

### Example: Defining and using a function
Start by defining a function that the agent can call. For instance, here's a fake snowfall tracking function:

Python

```
import json

def recent_snowfall(location: str) -> str:
	"""
	Fetches recent snowfall totals for a given location.
	:param location: The city name.
	:return: Snowfall details as a JSON string.
	"""
	mock_snow_data = {"Seattle": "0 inches", "Denver": "2 inches"}
	snow = mock_snow_data.get(location, "Data not available.")
	return json.dumps({"location": location, "snowfall": snow})
```
Register the function with your agent using the Azure AI SDK:

Python

```
# Define a function tool for the model to use
function_tool = FunctionTool(
	name="recent_snowfall",
	parameters={
		"type": "object",
		"properties": {
			"location": {"type": "string", "description": "The city name to check snowfall for."},
		},
		"required": ["location"],
		"additionalProperties": False
	},
	description="Get recent snowfall totals for a given location.",
	strict=True,
)

