"""
Microsoft Agent Framework - Agent with Tools Example

Demonstrates function calling and tool integration with the unified framework.
"""

from azure.ai.agents import Agent, AgentThread, Tool
from azure.ai.agents.models import MessageRole, ToolDefinition
import os
import json


def get_weather(location: str) -> str:
    """Get weather for a location"""
    # Mock weather data
    weather_data = {
        "Tokyo": {"temp": 22, "condition": "Sunny"},
        "London": {"temp": 15, "condition": "Rainy"},
        "New York": {"temp": 18, "condition": "Cloudy"}
    }
    data = weather_data.get(location, {"temp": 20, "condition": "Unknown"})
    return json.dumps(data)


def calculate(expression: str) -> str:
    """Perform calculation"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return str(result)
    except Exception as e:
        return f"Error: {e}"


def create_agent_with_tools():
    """Create agent with function tools"""
    
    # Define tools
    weather_tool = ToolDefinition(
        name="get_weather",
        description="Get current weather for a location",
        parameters={
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name"
                }
            },
            "required": ["location"]
        },
        function=get_weather
    )
    
    calc_tool = ToolDefinition(
        name="calculate",
        description="Perform mathematical calculations",
        parameters={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "Math expression to evaluate"
                }
            },
            "required": ["expression"]
        },
        function=calculate
    )
    
    # Create agent with tools
    agent = Agent(
        name="ToolAgent",
        instructions="You are a helpful assistant with access to weather and calculator tools.",
        model="gpt-4",
        tools=[weather_tool, calc_tool],
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    
    return agent


def run_tool_agent():
    """Run agent with tool calling"""
    try:
        agent = create_agent_with_tools()
        thread = AgentThread()
        
        # Test queries
        queries = [
            "What's the weather in Tokyo?",
            "Calculate 25 * 4 + 10"
        ]
        
        for query in queries:
            print(f"\n{'='*60}")
            print(f"User: {query}")
            print('='*60)
            
            thread.add_message(role=MessageRole.USER, content=query)
            response = agent.run(thread)
            
            # Get latest assistant message
            messages = thread.get_messages()
            for message in reversed(messages):
                if message.role == MessageRole.ASSISTANT:
                    print(f"Agent: {message.content}")
                    break
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires azure-ai-agents and Azure OpenAI credentials.")


if __name__ == "__main__":
    print("=== Microsoft Agent Framework - Tools Example ===")
    run_tool_agent()
