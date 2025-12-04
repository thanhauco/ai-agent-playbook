"""
OpenAI Agents SDK - Triage Agent Example

Demonstrates a production-ready triage pattern that routes to specialists.
"""

from openai import OpenAI
from typing import Optional
import json

client = OpenAI()


# Specialist functions
def handle_billing(issue: str) -> str:
    """Handle billing-related issues"""
    return json.dumps({
        "specialist": "billing",
        "message": f"Billing team will handle: {issue}",
        "ticket_id": "BILL-12345"
    })


def handle_technical(issue: str) -> str:
    """Handle technical issues"""
    return json.dumps({
        "specialist": "technical",
        "message": f"Technical support will handle: {issue}",
        "ticket_id": "TECH-67890"
    })


def handle_sales(query: str) -> str:
    """Handle sales inquiries"""
    return json.dumps({
        "specialist": "sales",
        "message": f"Sales team will handle: {query}",
        "lead_id": "LEAD-54321"
    })


def create_ticket(category: str, description: str, priority: str = "medium") -> str:
    """Create a support ticket"""
    return json.dumps({
        "ticket_id": f"TICKET-{id(description)}",
        "category": category,
        "priority": priority,
        "status": "created"
    })


# Triage agent configuration
triage_tools = [
    {
        "type": "function",
        "function": {
            "name": "handle_billing",
            "description": "Route to billing specialist for payment, invoice, or subscription issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "Billing issue description"}
                },
                "required": ["issue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_technical",
            "description": "Route to technical specialist for bugs, errors, or system issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "issue": {"type": "string", "description": "Technical issue description"}
                },
                "required": ["issue"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "handle_sales",
            "description": "Route to sales specialist for product inquiries or purchasing",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Sales query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a support ticket for general issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Issue category"},
                    "description": {"type": "string", "description": "Issue description"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]}
                },
                "required": ["category", "description"]
            }
        }
    }
]

available_functions = {
    "handle_billing": handle_billing,
    "handle_technical": handle_technical,
    "handle_sales": handle_sales,
    "create_ticket": create_ticket
}


def triage_agent(user_query: str) -> str:
    """Triage agent that routes queries to appropriate specialists"""
    messages = [
        {
            "role": "system",
            "content": (
                "You are a triage agent for customer support. Analyze each query and route it to the "
                "appropriate specialist: billing, technical, or sales. For general issues, create a ticket. "
                "Always be helpful and professional."
            )
        },
        {"role": "user", "content": user_query}
    ]
    
    # First API call
    response = client.chat.completions.create(
        model="gpt-4",
        messages=messages,
        tools=triage_tools
    )
    
    response_message = response.choices[0].message
    
    # Handle tool calls
    if response_message.tool_calls:
        for tool_call in response_message.tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(f"🔀 Routing to: {function_name}")
            print(f"📋 Arguments: {function_args}")
            
            # Execute the function
            function_response = available_functions[function_name](**function_args)
            
            # Add to messages
            messages.append(response_message)
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call.id,
                "name": function_name,
                "content": function_response
            })
        
        # Second API call
        final_response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        return final_response.choices[0].message.content
    
    return response_message.content


if __name__ == "__main__":
    test_queries = [
        "I was charged twice for my subscription",
        "The app keeps crashing when I try to upload files",
        "I want to upgrade to the enterprise plan",
        "My data export is taking too long"
    ]
    
    try:
        for i, query in enumerate(test_queries, 1):
            print(f"\n{'='*60}")
            print(f"Query {i}: {query}")
            print('='*60)
            result = triage_agent(query)
            print(f"\n✅ Final Response: {result}\n")
            
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires OPENAI_API_KEY.")
