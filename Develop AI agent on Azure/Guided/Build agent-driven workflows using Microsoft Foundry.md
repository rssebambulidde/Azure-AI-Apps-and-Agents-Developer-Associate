# Build agent-driven workflows using Microsoft Foundry

## Overview
This guide explains how to build and manage AI agent workflows in Microsoft Foundry. It's written for beginners and includes step-by-step explanations, examples, workflow patterns, Power Fx usage, maintenance tips, and a code integration section.

This guide is based on the conversation and training content about:
- Foundry workflows and node types
- Workflow patterns
- Creating workflows visually
- Adding agents and structured outputs
- Using Power Fx for logic and data handling
- Maintaining workflows with YAML and versioning
- Coding workflows with the Azure AI Projects SDK
- A practical workflow exercise for support ticket triage

---

## Table of Contents
1. What is a Foundry Workflow?
2. Workflow Patterns
3. Building Workflows in Foundry
4. Adding Agents to Workflows
5. Using Power Fx in Workflows
6. Maintaining Workflows
7. Invoking Workflows from Code
8. Practical Exercise: Customer Support Workflow
9. Exam Prep and Review

---

## 1. What is a Foundry Workflow?

A workflow in Microsoft Foundry is a visual sequence of connected actions. Each action is represented by a node. The nodes define steps such as invoking agents, evaluating conditions, transforming data, or interacting with users.

### Why workflows are useful
- They let you orchestrate AI reasoning without writing extensive code.
- They help connect multiple agents, logic, and runtime checks.
- They make it easier to understand and trace execution.
- They support real-world automation with human review and escalation.

### Core components
- **Nodes**: Building blocks of the workflow.
- **Variables**: Shared state that passes data between nodes.
- **Agent outputs**: Data returned by agents that influence behavior.
- **Connections**: Define execution paths and control flow.

### Example scenario
A support team receives many tickets. A workflow can:
- classify each ticket,
- decide whether to escalate or automate,
- continue processing tickets with consistent logic.

---

## 2. Workflow Patterns

Different tasks need different workflow structures. Foundry supports several patterns.

### Sequential workflow
- Runs in a fixed order.
- Each node passes output to the next.
- Good for pipelines like validation, enrichment, and final response.
- Ideal for beginners because it's easy to follow.

### Human-in-the-loop workflow
- Pauses to request user input or approval.
- Resumes after the user responds.
- Useful when human judgment or extra context is needed.
- Good for approval processes or low-confidence decisions.

### Group chat workflow
- Multiple agents collaborate dynamically.
- Control can shift based on context or results.
- Useful for complex support, multi-domain answers, or collaborative reasoning.
- Agents can build on each other's outputs.

### Key takeaway
Choose a pattern based on:
- how fixed the process is,
- whether people need to intervene,
- whether multiple agents need to coordinate.

---

## 3. Building Workflows in Foundry

Foundry provides a visual designer for workflows. You can start from a blank canvas or a predefined pattern.

### Visual workflow building
- Add nodes using the canvas.
- Move nodes to change layout.
- Configure each node directly.
- Save often because changes are not saved automatically.

### Main node types
- **Invoke**: Call an AI agent.
- **Flow**: Control execution using branches or loops.
- **Data transformation**: Set, reset, or parse variables.
- **Basic chat**: Send messages or ask questions.
- **End**: Finish the workflow and optionally return a result.

### What each node does
- **Invoke**: Runs an AI agent and returns text or structured output.
- **If/Else**: Branches based on conditions.
- **Go To**: Jumps to another node.
- **For Each**: Repeats actions for each item in a collection.
- **Set Variable**: Stores values for later use.
- **Parse Value**: Extracts data from structured outputs.

### Why this matters
Workflows are not just agent calls. They require careful use of data nodes, flow control nodes, and chat nodes to build complete automation.

---

## 4. Adding Agents to Workflows

Agents are the reasoning components that perform classification, decision-making, or response generation.

### How to add an agent
- Insert an **Invoke agent** node.
- Choose an existing agent or create a new one.
- Configure the agent's model, prompt, tools, knowledge, and guardrails.

### Why reuse agents
- Modular design: one agent for classification, another for response generation.
- Easier maintenance: update a single agent rather than many workflows.
- Better reuse: the same triage agent can be used across workflows.

### Structured outputs
- Agents can return JSON or JSON Schema, not just text.
- Structured outputs make downstream logic predictable.
- Use a response schema to enforce exact fields like `category`, `confidence`, or `customer_issue`.

### Storing agent output
- Save outputs into workflow variables.
- Example:
  - `Local.TriageOutputText`
  - `Local.TriageOutputJson`
- Later nodes read those variables to branch or make decisions.

### Practical agent use
- Use `Triage-Agent` to classify ticket category and confidence.
- Use `Resolution-Agent` to draft a response for non-billing tickets.
- Use structured JSON for reliable condition checks.

---

## 5. Using Power Fx in Workflows

Power Fx is the low-code formula language used inside workflows.

### What Power Fx does
- Evaluates conditions.
- Manipulates data.
- Controls workflow flow.
- Works with system and local variables.

### Variable types
- **System variables**: Contextual values like the last message or user info.
- **Local variables**: Values created during workflow execution.

### Common Power Fx examples
| Purpose | Formula | Notes |
|---|---|---|
| Uppercase text | `Upper(Local.Input)` | Convert text to all caps |
| Lowercase text | `Lower(Local.Input)` | Convert text to all lower case |
| String length | `Len(Local.Input)` | Number of characters |
| Confidence check | `Local.Confidence > 0.8` | Used in If/Else nodes |
| Conditional value | `If(Local.Confidence > 0.8, "Proceed", "Escalate")` | Return one of two values |
| Sum numbers | `Sum([10, 20, 30])` | Adds simple list values |
| Sum column | `Sum(Local.ItemList, Amount)` | Adds the Amount field across records |
| Count items | `Count(Local.ItemList)` | Number of records in a table or list |
| Blank check | `IsBlank(Local.Input)` | True when input is empty |
| Empty table | `IsEmpty(Local.ItemList)` | True when a table has no records |
| Loop map | `ForAll(Local.ItemList, Upper(Name))` | Apply a formula to each list item |
| Concatenate | `Concatenate(Local.FirstName, " ", Local.LastName)` | Join text strings |

### Using formulas for decisions
- In **If/Else** nodes, formulas decide which path runs.
- Example for confidence: `Local.TriageOutputJson.confidence > 0.6`
- Example for category: `Local.TriageOutputJson.category = "Billing"`

### Using formulas in loops
- Use **For Each** to loop through collections.
- Use `Local.CurrentTicket` or loop variables inside the loop.
- Combine loops with conditions to avoid repeated nodes.

### Practical note
Power Fx is the glue. It lets your workflow react to agent outputs, user input, and system state without full programming.

---

## 6. Maintaining Workflows

A workflow is not finished when it works. Maintenance keeps it reliable and understandable.

### Visual and YAML representations
- Workflows appear in a visual canvas and in YAML.
- The canvas is useful for design and tracing execution.
- YAML is useful for advanced edits, source control, and diffs.
- Changes in either view stay in sync.

### Versioning
- Foundry saves an immutable version every time you save.
- Use version history to compare changes and roll back if needed.
- Versioning helps collaboration and audit.

### Notes and documentation
- Attach notes to nodes or workflow sections.
- Notes explain decisions, thresholds, and variable use.
- Good documentation helps future maintainers understand the workflow.

### Best practices
- Review workflows regularly for unused or redundant nodes.
- Keep structured outputs consistent.
- Document complex logic clearly.
- Use version history for validation and rollback.
- Keep the workflow clear and efficient.

### Maintainer checklist
- Confirm visual and YAML match.
- Verify outputs are stored and referenced correctly.
- Remove unused nodes.
- Add notes to explain hard decisions.
- Save versions before major edits.
- Use source control when possible.

---

## 7. Invoking Workflows from Code

You can run a Foundry workflow from an application using the Azure AI Projects SDK.

### Why code integration matters
- Embed workflows in web apps, APIs, backends, or batch jobs.
- Reuse workflow logic without rebuilding it in code.
- Combine visual design with programmatic execution.

### How invocation works
1. Create a Foundry workflow visually.
2. Save it and reference its name.
3. Connect to Foundry with `AIProjectClient`.
4. Create a conversation context.
5. Invoke the workflow by name.

### Python example pattern
```python
workflow_name = "triage-workflow"
conversation = openai_client.conversations.create()
stream = openai_client.responses.create(
    conversation=conversation.id,
    extra_body={"agent": {"name": workflow_name, "type": "agent_reference"}},
    input="Users can't reset their password from the mobile app.",
    stream=True,
)
```

### Streaming events
- `response.completed`: Workflow finished and final output is available.
- `response.output_item.done`: A workflow action completed.

Example event handling:
```python
for event in stream:
    if event.type == "response.completed":
        print("Workflow completed:")
        for message in event.response.output:
            if message.content:
                for content_item in message.content:
                    if content_item.type == 'output_text':
                        print(content_item.text)
    if (event.type == "response.output_item.done") and event.item.type == ItemType.WORKFLOW_ACTION:
        print(f"Action '{event.item.action_id}' completed with status: {event.item.status}")
```

### Human-in-the-loop behavior
- Workflows may pause while waiting for user input.
- Your app can send additional messages to continue execution.

### Benefits of integration
- Web applications can call workflows directly.
- APIs can expose workflow automation.
- Batch jobs can process many items.
- Testing and CI/CD can validate workflows programmatically.
- Custom UIs can present workflow-driven user experiences.

---

## 8. Practical Exercise: Customer Support Workflow

This example walks through a complete workflow to triage customer support tickets.

### Exercise overview
The workflow:
- starts with an array of support tickets,
- loops over each ticket,
- classifies it into Billing, Technical, or General,
- handles low-confidence cases,
- routes billing tickets to escalation,
- generates a response for non-billing tickets.

---

## 9. Exam Prep and Review

This file contains exam prep content and practice questions to help learners review key concepts.

---

## Final Tips for Beginners
- Start simple with sequential workflows.
- Use local variables to capture agent outputs.
- Test the workflow frequently as you build it.
- Add notes to explain any complex logic.
- Keep a copy of workflow YAML in source control if possible.
- Practice with the example workflow and then adapt it to your own scenario.

Good luck learning Microsoft Foundry workflows and preparing for your exam!