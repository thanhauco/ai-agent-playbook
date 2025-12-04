"""
Pydantic AI Basic Agent Example

Pydantic AI is a type-safe, production-grade framework for building AI agents.
It uses Pydantic models for structured inputs/outputs and validation.
"""

from pydantic_ai import Agent
from pydantic import BaseModel
from typing import Optional

# Note: Install with: pip install pydantic-ai


class CityInfo(BaseModel):
    """Structured output for city information"""
    city: str
    country: str
    population: Optional[int] = None
    description: str


# Create a type-safe agent
agent = Agent(
    'openai:gpt-4',
    result_type=CityInfo,
    system_prompt=(
        'You are a helpful assistant that provides information about cities. '
        'Always return structured data with the city name, country, and a brief description.'
    ),
)


def run_basic_agent():
    """Run the basic Pydantic AI agent"""
    try:
        # Query the agent - it will return a validated CityInfo object
        result = agent.run_sync('Tell me about Tokyo')
        
        print(f"City: {result.data.city}")
        print(f"Country: {result.data.country}")
        print(f"Description: {result.data.description}")
        
        # The result is fully typed and validated
        assert isinstance(result.data, CityInfo)
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'pydantic-ai' installed and OPENAI_API_KEY set.")


if __name__ == "__main__":
    run_basic_agent()
