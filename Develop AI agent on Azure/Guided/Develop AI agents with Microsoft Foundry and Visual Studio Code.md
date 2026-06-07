# Develop AI agents with Microsoft Foundry and Visual Studio Code

## Overview
This guide helps beginners learn how to develop AI agents using Microsoft Foundry and Visual Studio Code. It combines portal-based concepts with VS Code development workflow, practical examples, and exam-ready review notes.

This guide covers:
- What AI agents are and why they matter
- Foundry Agent Service basics
- Portal vs VS Code development
- Creating and testing agents
- Working with custom tools and data
- Running agents from code
- Best practices, security, and exam preparation

---

## Table of Contents
1. What is an AI agent?
2. Microsoft Foundry Agent Service
3. Portal-based agent development
4. VS Code development workflow
5. Building your first agent
6. Adding grounding data and tools
7. Testing and validating agents
8. Invoking agents from code
9. Security and maintenance
10. Exam prep and practice

---

## 1. What is an AI agent?

An AI agent is more than a chat model. It is a system that understands user intent, maintains context, and can take actions using tools or integrations.

### Key capabilities
- Understands natural language inputs
- Maintains multi-turn context
- Uses tools and APIs to get real data or perform actions
- Can follow defined instructions and business logic

### Why agents matter
- Automate repetitive tasks
- Improve response consistency
- Scale support, research, and productivity workflows
- Enable safer and more predictable AI behavior through tooling

---

## 2. Microsoft Foundry Agent Service

Microsoft Foundry Agent Service is a managed platform for building and running AI agents.

### What it provides
- Portal and low-code experiences for quick agent setup
- VS Code integration for source control and code-first workflows
- Secure storage of conversation state and data
- Support for tools, functions, and OpenAPI integrations

### Important concepts
- **Agent**: The entity that processes prompts and makes decisions.
- **Tool**: A custom capability the agent can call.
- **Workflow**: A visual orchestration of agent and logic steps.
- **Project**: Container for agent resources and configurations.

---

## 3. Portal-based agent development

The Foundry portal is great for beginners and rapid prototyping.

### Portal strengths
- Visual agent builder and playground
- Easy access to agent settings and instructions
- Built-in tool registration and testing
- Quick grounding with files, knowledge, and documents

### Typical portal workflow
1. Create a new project in the Foundry portal.
2. Build an agent with instructions and model settings.
3. Add tools, files, or knowledge sources.
4. Test in the playground.
5. Save and publish the agent.

---

## 4. VS Code development workflow

Visual Studio Code is ideal for versioned development and collaboration.

### Why use VS Code
- Keep agent YAML in source control
- Edit agent definitions as code
- Use the Foundry Toolkit extension to manage resources
- Integrate with Git, CI/CD, and deployment pipelines

### Setup steps
1. Install VS Code.
2. Install the Foundry Toolkit extension.
3. Sign in to Azure from the extension.
4. Connect to your Foundry project.
5. Open agent and workflow YAML definitions in the editor.

---

## 5. Building your first agent

### Core agent structure
An agent definition typically includes:
- `name`
- `description`
- `model`
- `instructions`
- `tools`
- `metadata`

### Simple agent example
Create an agent that answers FAQs:
- Define clear system and user instructions.
- Keep the prompt focused on the task.
- Set model parameters such as temperature.

### Step-by-step
1. In the portal, create a new agent.
2. Add instructions explaining the agent’s role.
3. Choose a model that fits your use case.
4. Save and test the agent with sample prompts.

---

## 6. Adding grounding data and tools

### Grounding data
Grounding data helps the agent answer questions based on real documents or files.

Examples:
- Policies in a text file
- Product manuals
- CSV data for analysis

### Adding tools
Custom tools enable agents to call code or APIs.

Tool options:
- **Function calling**: Lightweight local functions.
- **Azure Functions**: Serverless actions.
- **OpenAPI tools**: Typed API integrations.

### Example tools
- `get_order_status(order_id)`
- `create_support_ticket(payload)`
- `lookup_inventory(item_id)`

### Use case
A support agent can use a `get_order_status` tool to answer delivery questions accurately instead of guessing.

---

## 7. Testing and validating agents

### In the portal
- Use the built-in playground.
- Try different prompt variations.
- Check if the agent uses tools correctly.

### In VS Code
- Edit agent YAML and validate the syntax.
- Use the extension to open the agent playground.
- Keep tests repeatable in source control.

### Test categories
- **Happy path**: Expected user requests.
- **Edge cases**: Unclear or malformed prompts.
- **Tool invocation**: Ensure correct parameter passing.
- **Failure handling**: Verify graceful error behavior.

---

## 8. Invoking agents from code

Integrate agents into applications using the Azure AI Projects SDK.

### Basic flow
1. Authenticate with Azure.
2. Create a project client.
3. Create a conversation.
4. Invoke the agent or workflow.
5. Process responses.

### Python example
```python
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

endpoint = "https://your-foundry-endpoint"
credential = DefaultAzureCredential()

with AIProjectClient(endpoint=endpoint, credential=credential) as project_client:
    with project_client.get_openai_client() as openai_client:
        conversation = openai_client.conversations.create()
        stream = openai_client.responses.create(
            conversation=conversation.id,
            extra_body={"agent": {"name": "my-agent", "type": "agent_reference"}},
            input="Hello, I need help with my order.",
            stream=True,
        )
        for event in stream:
            if event.type == "response.completed":
                print("Workflow completed")
```

---

## 9. Security and maintenance

### Security best practices
- Never store secrets in agent YAML or code.
- Use Azure Key Vault or secure environment storage.
- Restrict access with RBAC.
- Use allowlists for external services.

### Maintenance
- Keep agent definitions version controlled.
- Document tool behavior and decision logic.
- Regularly review and remove unused tools or instructions.
- Monitor usage and costs.

---

## 10. Exam prep and practice

### Key concepts to remember
- Difference between portal and VS Code development.
- The role of tools, workflows, and grounding data.
- How custom tools change an agent from a text-only model to an action-capable service.
- The importance of security and version control.

### Practice questions
1. What are the main differences between portal and VS Code workflows?
2. When should you use a custom tool instead of a prompt-only agent?
3. What is the role of grounding data in an AI agent?
4. How do you safely manage secrets for agents and tools?
5. What is the purpose of `response.completed` in a streamed workflow?

---

## Final tips for beginners
- Start with small, focused agents.
- Use the portal to learn and VS Code to scale.
- Keep instructions clear and concise.
- Test tools and code paths often.
- Document your agent decisions and tool usage.

Good luck building AI agents with Microsoft Foundry and Visual Studio Code!