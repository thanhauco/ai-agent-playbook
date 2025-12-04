"""
Modern Function Calling Patterns (2025)

Demonstrates current best practices for function calling with structured outputs.
"""

from openai import OpenAI
from pydantic import BaseModel
from typing import List, Literal
import json

client = OpenAI()


# Define structured output schemas using Pydantic
class WeatherInfo(BaseModel):
    location: str
    temperature: float
    unit: Literal["celsius", "fahrenheit"]
    condition: str
    humidity: int


class SearchResult(BaseModel):
    query: str
    results: List[dict]
    total_found: int


# Function implementations
def get_current_weather(location: str, unit: str = "celsius") -> str:
    """Mock weather function"""
    weather = WeatherInfo(
        location=location,
        temperature=22.5 if unit == "celsius" else 72.5,
        unit=unit,
        condition="sunny",
        humidity=65
    )
    return weather.model_dump_json()


def search_web(query: str, max_results: int = 5) -> str:
    """Mock search function"""
    result = SearchResult(
        query=query,
        results=[
            {"title": f"Result {i}", "url": f"https://example.com/{i}"}
            for i in range(max_results)
        ],
        total_found=max_results
    )
    return result.model_dump_json()


# Tool definitions with strict schema
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get the current weather in a location",
            "strict": True,  # Enable strict schema validation (2025 feature)
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA"
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit"
                    }
                },
                "required": ["location"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information",
            "strict": True,
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "max_results": {
                        "type": "integer",
                        "description": "Maximum number of results",
                        "minimum": 1,
                        "maximum": 10
                    }
                },
                "required": ["query"],
                "additionalProperties": False
            }
        }
    }
]

available_functions = {
    "get_current_weather": get_current_weather,
    "search_web": search_web
}


def run_with_function_calling(query: str):
    """Modern function calling with structured outputs"""
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": query}
    ]
    
    print(f"Query: {query}\n")
    
    # Call with parallel function calling (2025 default)
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        parallel_tool_calls=True  # Enable parallel execution
    )
    
    response_message = response.choices[0].message
    
    # Handle multiple tool calls in parallel
    if response_message.tool_calls:
        print(f"🔧 Executing {len(response_message.tool_calls)} tool(s)...")
        messages.append(response_message)
        
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"  ➜ {function_name}({function_args})")
            
            # Execute function
            function_response = available_functions[function_name](**function_args)
            
            # Validate response is valid JSON
            try:
                json.loads(function_response)
            except json.JSONDecodeError:
                print(f"  ⚠️  Invalid JSON response from {function_name}")
            
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response
            })
        
        # Get final response
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        print(f"\n✅ Final Response: {final_response.choices[0].message.content}\n")
        return final_response.choices[0].message.content
    
    return response_message.content


if __name__ == "__main__":
    try:
        # Test parallel function calling
        run_with_function_calling(
            "What's the weather in Tokyo and search for 'AI agents 2025'"
        )
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Requires OPENAI_API_KEY.")
