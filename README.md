# AI Agent Playbook Study Project

This repository contains code examples extracted from "The AI Agent Playbook" by Bhanu Chaddha. The examples are organized by framework to help you study and understand the different approaches to building AI agents.

## Structure

- **langchain/**: Examples using the LangChain framework (Chains, Agents, Memory, RAG).
- **crewai/**: Examples using CrewAI for multi-agent teams.
- **autogen/**: Examples using Microsoft AutoGen for conversational agents.
- **langgraph/**: Examples using LangGraph for complex, stateful workflows.
- **pydantic_ai/**: Type-safe agents with Pydantic validation (2025).
- **openai_agents/**: OpenAI Agents SDK with handoffs and routing (2025).
- **llamaindex/**: LlamaIndex RAG-focused agents and workflows (2025).
- **microsoft_agents/**: Microsoft Agent Framework (unified Semantic Kernel + AutoGen, 2025).
- **mcp/**: Examples for Model Context Protocol (MCP) servers and clients.
- **a2a/**: Examples for Agent-to-Agent (A2A) protocol and agent cards.
- **advanced/**: Advanced patterns (function calling, streaming, memory).

## Usage

Each directory contains Python scripts representing the examples from the book. You may need to install the respective libraries to run them:

```bash
pip install langchain crewai pyautogen langgraph pydantic-ai llama-index openai chromadb tiktoken httpx
```

> [!NOTE]
> You will likely need API keys (e.g., `OPENAI_API_KEY`) set in your environment for these agents to function.
