"""
OpenAI Agents SDK - Basic Agent Example

The OpenAI Agents SDK is the production-ready successor to Swarm.
It provides minimal primitives for building agentic workflows.
"""

from openai import OpenAI
import json

# Note: Install with: pip install openai>=1.0.0

client = OpenAI()  # Requires OPENAI_API_KEY environment variable


def get_weather(location: str) -> str:
    """Get weather for a location (mock implementation)"""
    return json.dumps({
        "location": location,
        "temperature": "72°F",
        "condition": "sunny"
    })


def calculate(expression: str) -> str:
    """Perform calculation"""
    try:
        result = eval(expression, {"__builtins__": {}}, {})
        return json.dumps({"result": result})
    except:
        return json.dumps({"error": "Invalid expression"})


# Define tools
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get current weather for a location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name or coordinates"
                    }
                },
                "required": ["location"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "Perform mathematical calculations",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Math expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]

# Tool function mapping
available_tools = {
    "get_weather": get_weather,
    "calculate": calculate
}


def run_agent(query: str):
    """Run the OpenAI agent with function calling"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant with access to tools."},
        {"role": "user", "content": query}
    ]
    
    # First API call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools
    )
    
    response_message = response.choices[0].message
    messages.append(response_message)
    
    # Handle tool calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            # Execute the function
            function_response = available_tools[function_name](**function_args)
            
            # Add function response to messages
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response
            })
        
        # Second API call with function results
        second_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return second_response.choices[0].message.content
    
    return response_message.content


if __name__ == "__main__":
    try:
        result = run_agent("What's the weather in Tokyo and what is 25 * 4?")
        print(f"Agent Response: {result}")
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires OPENAI_API_KEY environment variable.")
