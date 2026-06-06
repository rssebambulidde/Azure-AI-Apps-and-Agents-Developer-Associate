# Azure AI Apps and Agents Developer Associate (beta)

## Module 1: Introduction

### Core concept
- Microsoft Foundry Agent Service lets you build AI agents without managing infrastructure.
- Works through portal UI or Visual Studio Code extension.

### Why it matters
- Helps automate tasks like patient inquiries and appointment scheduling.
- Provides enterprise-grade security and managed storage.

### What you should remember
- Foundry supports both low-code portal and code-based VS Code workflows.
- The service handles compute, storage, and secure conversation state.
- Good for building production-ready agents faster.

---

## Module 2: Understand AI Agents and Microsoft Foundry Agent Service

### What an AI agent is
- A service that uses generative AI to understand intent, make decisions, and perform tasks.
- More than a chat model: it can use tools, maintain context, and act autonomously.

### Why agents are useful
- Automate repetitive work
- Help with decision-making
- Scale without extra people
- Be available 24/7

### Common use cases
- Productivity assistants
- Research agents
- Sales automation
- Customer service bots
- Developer helpers like GitHub Copilot

### Security risks
- Data leakage
- Prompt injection
- Unauthorized access
- Data poisoning
- Supply chain vulnerabilities
- Unsafe autonomous actions
- Poor logging
- Model output leakage

### Mitigation strategies
- Use RBAC and least privilege
- Filter and validate prompts
- Gate sensitive actions with human review
- Log everything and audit frequently
- Keep data and models refreshed and clean

### Foundry overview
- Fully managed platform for declarative and hosted agents
- Supports prompt-based agents, workflow agents, and hosted container agents
- Built-in tool catalog and secure data handling
- Good for enterprise use and production deployments

---

## Module 3: Explore Development Approaches

### Foundry portal
Best for:
- quick prototyping
- visual configuration
- stakeholder review
- centralized agent management and dashboards

### Visual Studio Code
Best for:
- developer workflows
- version control
- direct YAML editing
- production-grade projects

### Common workflow
1. Connect to Foundry
2. Create agent
3. Configure instructions
4. Add tools
5. Test
6. Iterate
7. Deploy
8. Integrate

### Required Azure resources
- Foundry project
- Model deployments

### Optional Azure services
- Azure AI Search
- Azure Storage
- Azure Key Vault
- Azure Functions

### How to choose
- Use portal for visual design and fast experimentation
- Use VS Code for versioned, code-centric development
- Many teams combine both

---

## Module 4: Build Your First Agent in Microsoft Foundry

### Portal creation steps
1. Go to https://ai.azure.com
2. Select or create a Foundry project
3. Build > Agents > Create
4. Provide name, description, and model

### Agent configuration
- System instructions define behavior and tone
- Temperature and top_p control response style
- Good instructions improve reliability

### Testing
- Use the built-in playground
- Test multi-turn conversations
- Validate tool use and context handling

### Tools
- Configured tools: built-in ready-to-use
- Catalog tools: additional available services
- Custom tools: your OpenAPI or MCP tools

### Deployment
- Save and deploy from portal
- Foundry gives connection info for integration

---

## Module 5: Set Up Visual Studio Code for Agent Development

### VS Code extension benefits
- Manage Foundry resources inside VS Code
- Edit agents visually or via YAML
- Support for model deployments, tools, vector stores, and playgrounds

### Installation
- Search “Microsoft Foundry” in Extensions
- Install the extension

### Connect to Azure
- Sign in through Azure view
- Expand subscription and Foundry project
- Open project in Foundry extension

### Prepare resources
- Deploy a model if needed
- Model deployments must exist before agent config

### Agent management
- Agents created in portal appear in VS Code
- Save changes directly to Foundry
- Compare multiple agents and use Git tracking

---

## Module 6: Configure and Manage Agents in Visual Studio Code

### Key properties
- Agent name and description
- Model deployment selection
- System instructions
- Temperature and top_p
- Agent ID and metadata

### YAML structure
- version
- name
- description
- id
- metadata
- model
- instructions
- tools

### Why edit YAML
- Better version control
- Easier bulk changes
- Templates and automation
- Clear code review process

### Best practices
- Keep YAML in Git
- Use clear names and tags
- Comment complex logic
- Test after changes
- Start simple then iterate
- Keep instructions narrow

---

## Module 7: Extend Agent Capabilities with Tools

### What tools do
- Tools let agents act on data, execute tasks, and fetch real-time info
- Agent selects tools automatically when needed
- Tool results are built into responses

### Common tools
- Code Interpreter
- File Search
- Bing Web Search
- Azure AI Search
- OpenAPI-based integrations

### How tool calling works
1. User sends request
2. Agent decides tool usage
3. Tool executes
4. Results return
5. Agent responds

### Adding tools
- Use visual designer or YAML
- Some tools require additional config like connection IDs or vector stores

### MCP servers
- Standardized integration protocol
- Remote, local, or custom servers
- Good for reusable or enterprise tools

### Tool best practices
- Start with built-in tools first
- Choose tools only when needed
- Tell the agent how/when to use each tool
- Keep knowledge sources current
- Test tool invocation carefully

---

## Module 8: Test, Deploy, and Integrate Agents

### Testing approaches
- Happy path
- Edge cases
- Out-of-scope requests
- Multi-turn context
- Tool invocation verification

### Deploying
- Save agent configuration to Foundry
- For hosted agents, deploy from VS Code build menu

### Publishing
- Creates Agent Application endpoint
- Provides stable external URL
- Uses Entra ID authentication
- Requires Azure AI User role

### Endpoint details
- Uses Responses API protocol
- Endpoint remains stable across version updates
- No API key auth for published agent apps

### Updating published agents
- Make changes, test, and publish updates
- Existing endpoint stays the same

### Integration patterns
- Web apps
- Backend APIs
- Chatbot UIs
- Scheduled automation

### Production focus
- Monitor latency, tool success, token usage
- Enforce least privilege
- Implement retries and validation
- Store conversation history client-side for multi-turn flows

---

## Exam Study Tips
- Know the difference between portal vs VS Code workflows
- Understand agent types: prompt-based, workflow, hosted
- Memorize key tools and when to use them
- Focus on Foundry security concepts and mitigation
- Learn deployment vs publish lifecycle
- Be comfortable with agent YAML structure
- Understand authentication and RBAC for published agents
