"""
LlamaIndex - Simple ReAct Agent Example

LlamaIndex is a RAG-focused framework with excellent agent capabilities.
This example shows a basic ReAct agent with tools.
"""

from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.core.tools import FunctionTool

# Note: Install with: pip install llama-index llama-index-llms-openai


def multiply(a: float, b: float) -> float:
    """Multiply two numbers"""
    return a * b


def add(a: float, b: float) -> float:
    """Add two numbers"""
    return a + b


def weather_lookup(city: str) -> str:
    """Get weather for a city (mock)"""
    return f"The weather in {city} is sunny and 72°F"


def run_simple_agent():
    """Run a simple LlamaIndex ReAct agent"""
    try:
        # Create tools from functions
        multiply_tool = FunctionTool.from_defaults(fn=multiply)
        add_tool = FunctionTool.from_defaults(fn=add)
        weather_tool = FunctionTool.from_defaults(fn=weather_lookup)
        
        # Initialize LLM
        llm = OpenAI(model="gpt-4")
        
        # Create ReAct agent
        agent = ReActAgent.from_tools(
            [multiply_tool, add_tool, weather_tool],
            llm=llm,
            verbose=True
        )
        
        # Query the agent
        response = agent.chat("What is (3 + 5) * 2? Also, what's the weather in Tokyo?")
        
        print(f"\nAgent Response: {response}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'llama-index' and OPENAI_API_KEY.")


if __name__ == "__main__":
    run_simple_agent()
