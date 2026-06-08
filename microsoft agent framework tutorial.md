# Microsoft Agent Framework

## Simple summary

Microsoft Agent Framework is a toolkit for building AI agents and multi-agent workflows in Python.

It helps developers create:
- individual agents that use LLMs,
- tools and MCP integrations,
- and graph-based workflows that connect agents and functions.

The framework also includes:
- model clients,
- session state management,
- context providers for memory,
- middleware,
- and MCP clients for tool integration.

## What it is used for

Use Agent Framework when you want to build interactive and reliable AI applications.

It is best for:
- open-ended or conversational tasks,
- tasks that need tool use,
- and multi-step workflows with multiple agents or functions.

## Quick start

You can install it with:

```bash
pip install agent-framework
```

A simple Python example creates a Foundry chat client, connects it to Azure, and makes an agent that responds to user input.

## Agents vs workflows

Use an agent when:
- the task is conversational,
- you want autonomous tool use,
- or one LLM call is enough.

Use a workflow when:
- the task has clear steps,
- multiple agents or functions must work together,
- or you need explicit control over the order of execution.

## Why it is important

Microsoft Agent Framework combines the simple agent ideas from AutoGen with enterprise features from Semantic Kernel, such as:
- session-based state,
- type safety,
- middleware,
- telemetry,
- and strong multi-agent orchestration.

It is positioned as the next generation of both technologies.

## Key takeaway

Microsoft Agent Framework is a powerful SDK for building AI agents and workflows that are flexible, scalable, and suitable for production applications.
