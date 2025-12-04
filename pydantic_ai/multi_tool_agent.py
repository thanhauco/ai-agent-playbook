"""
Pydantic AI Multi-Tool Agent Example

Demonstrates tool integration with type-safe function calling.
"""

from pydantic_ai import Agent, RunContext
from pydantic import BaseModel
from dataclasses import dataclass
import httpx

# Note: Install with: pip install pydantic-ai httpx


@dataclass
class SearchDeps:
    """Dependencies for the agent (can include API clients, databases, etc.)"""
    http_client: httpx.AsyncClient


class SearchResult(BaseModel):
    """Structured search result"""
    query: str
    summary: str
    sources: list[str]


# Create agent with dependencies
agent = Agent(
    'openai:gpt-4',
    result_type=SearchResult,
    deps_type=SearchDeps,
    system_prompt='You are a research assistant. Use tools to gather information.',
)


@agent.tool
async def search_web(ctx: RunContext[SearchDeps], query: str) -> str:
    """
    Search the web for information.
    
    Args:
        query: The search query
        
    Returns:
        Search results as text
    """
    # Mock search for demonstration
    # In production, this would call a real search API
    return f"Mock search results for: {query}"


@agent.tool
async def get_weather(ctx: RunContext[SearchDeps], location: str) -> dict:
    """
    Get weather information for a location.
    
    Args:
        location: City name or coordinates
        
    Returns:
        Weather data
    """
    # Mock weather data
    return {
        "location": location,
        "temperature": 72,
        "condition": "sunny",
        "humidity": 65
    }


@agent.tool
async def calculate(ctx: RunContext[SearchDeps], expression: str) -> float:
    """
    Perform mathematical calculations.
    
    Args:
        expression: Math expression to evaluate
        
    Returns:
        Calculation result
    """
    try:
        # Safe evaluation (in production, use a proper math parser)
        result = eval(expression, {"__builtins__": {}}, {})
        return float(result)
    except Exception as e:
        return 0.0


async def run_multi_tool_agent():
    """Run the multi-tool agent"""
    try:
        async with httpx.AsyncClient() as client:
            deps = SearchDeps(http_client=client)
            
            # Agent will use tools as needed
            result = await agent.run(
                'What is the weather in Tokyo and what is 25% of 200?',
                deps=deps
            )
            
            print(f"Query: {result.data.query}")
            print(f"Summary: {result.data.summary}")
            print(f"Sources: {', '.join(result.data.sources)}")
            
            # Show which tools were called
            print(f"\nTools called: {len(result.all_messages())} total messages")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'pydantic-ai', 'httpx', and OPENAI_API_KEY.")


if __name__ == "__main__":
    import asyncio
    asyncio.run(run_multi_tool_agent())
