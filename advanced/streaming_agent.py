"""
Streaming Agent Responses (2025)

Demonstrates real-time streaming of agent responses and tool calls.
"""

from openai import OpenAI
import json

client = OpenAI()


def get_stock_price(symbol: str) -> str:
    """Mock stock price lookup"""
    prices = {"AAPL": 185.50, "GOOGL": 140.25, "MSFT": 380.75}
    price = prices.get(symbol.upper(), 100.00)
    return json.dumps({"symbol": symbol, "price": price, "currency": "USD"})


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_stock_price",
            "description": "Get current stock price for a symbol",
            "parameters": {
                "type": "object",
                "properties": {
                    "symbol": {"type": "string", "description": "Stock ticker symbol"}
                },
                "required": ["symbol"]
            }
        }
    }
]

available_functions = {"get_stock_price": get_stock_price}


def stream_agent_response(query: str):
    """Stream agent responses in real-time"""
    messages = [
        {"role": "system", "content": "You are a helpful financial assistant."},
        {"role": "user", "content": query}
    ]
    
    print(f"User: {query}\n")
    print("Agent: ", end="", flush=True)
    
    # Stream the response
    stream = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=tools,
        stream=True
    )
    
    tool_calls = []
    current_tool_call = None
    
    for chunk in stream:
        delta = chunk.choices[0].delta
        
        # Handle text streaming
        if delta.content:
            print(delta.content, end="", flush=True)
        
        # Handle tool call streaming
        if delta.tool_calls:
            for tool_call_chunk in delta.tool_calls:
                # Initialize new tool call
                if current_tool_call is None or tool_call_chunk.index != current_tool_call.get("index"):
                    if current_tool_call:
                        tool_calls.append(current_tool_call)
                    current_tool_call = {
                        "index": tool_call_chunk.index,
                        "id": tool_call_chunk.id or "",
                        "type": "function",
                        "function": {
                            "name": tool_call_chunk.function.name or "",
                            "arguments": ""
                        }
                    }
                
                # Accumulate function arguments
                if tool_call_chunk.function.arguments:
                    current_tool_call["function"]["arguments"] += tool_call_chunk.function.arguments
    
    # Add last tool call if exists
    if current_tool_call:
        tool_calls.append(current_tool_call)
    
    print("\n")
    
    # Execute tool calls if any
    if tool_calls:
        print(f"\n🔧 Executing {len(tool_calls)} tool call(s)...")
        
        for tool_call in tool_calls:
            function_name = tool_call["function"]["name"]
            function_args = json.loads(tool_call["function"]["arguments"])
            
            print(f"  ➜ {function_name}({function_args})")
            result = available_functions[function_name](**function_args)
            print(f"  ✓ Result: {result}")
            
            # Add tool response to messages
            messages.append({
                "role": "assistant",
                "content": None,
                "tool_calls": [tool_call]
            })
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call["id"],
                "name": function_name,
                "content": result
            })
        
        # Stream final response with tool results
        print("\nAgent (with results): ", end="", flush=True)
        final_stream = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            stream=True
        )
        
        for chunk in final_stream:
            if chunk.choices[0].delta.content:
                print(chunk.choices[0].delta.content, end="", flush=True)
        
        print("\n")


if __name__ == "__main__":
    try:
        queries = [
            "What's the current price of Apple stock?",
            "Compare GOOGL and MSFT stock prices"
        ]
        
        for query in queries:
            print("="*60)
            stream_agent_response(query)
            print()
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Requires OPENAI_API_KEY.")
