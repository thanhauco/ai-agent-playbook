"""
OpenAI Agents SDK - Handoff Demo

Demonstrates agent-to-agent handoffs for multi-agent collaboration.
Based on OpenAI's Agents SDK pattern (successor to Swarm).
"""

from openai import OpenAI
from typing import Dict, List, Callable
import json

client = OpenAI()


# Define transfer functions (handoffs)
def transfer_to_sales() -> Dict:
    """Transfer conversation to sales agent"""
    return {"agent": "sales_agent"}


def transfer_to_support() -> Dict:
    """Transfer conversation to support agent"""
    return {"agent": "support_agent"}


def transfer_to_triage() -> Dict:
    """Transfer back to triage agent"""
    return {"agent": "triage_agent"}


# Agent configurations
agents = {
    "triage_agent": {
        "name": "Triage Agent",
        "instructions": (
            "You are a triage agent. Determine if the user needs sales or support. "
            "Use transfer_to_sales for purchasing questions. "
            "Use transfer_to_support for technical issues."
        ),
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "transfer_to_sales",
                    "description": "Transfer to sales agent for purchase inquiries"
                }
            },
            {
                "type": "function",
                "function": {
                    "name": "transfer_to_support",
                    "description": "Transfer to support agent for technical help"
                }
            }
        ]
    },
    "sales_agent": {
        "name": "Sales Agent",
        "instructions": (
            "You are a sales agent. Help with product information and purchasing. "
            "Be enthusiastic and helpful. You can transfer back to triage if needed."
        ),
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "transfer_to_triage",
                    "description": "Transfer back to triage"
                }
            }
        ]
    },
    "support_agent": {
        "name": "Support Agent",
        "instructions": (
            "You are a technical support agent. Help troubleshoot issues. "
            "Be patient and thorough. You can transfer back to triage if needed."
        ),
        "tools": [
            {
                "type": "function",
                "function": {
                    "name": "transfer_to_triage",
                    "description": "Transfer back to triage"
                }
            }
        ]
    }
}

# Function mapping
available_functions = {
    "transfer_to_sales": transfer_to_sales,
    "transfer_to_support": transfer_to_support,
    "transfer_to_triage": transfer_to_triage
}


def run_multi_agent(query: str, max_turns: int = 10):
    """Run multi-agent system with handoffs"""
    current_agent = "triage_agent"
    messages = [{"role": "user", "content": query}]
    
    for turn in range(max_turns):
        agent_config = agents[current_agent]
        print(f"\n🤖 [{agent_config['name']}]")
        
        # Call OpenAI API
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": agent_config["instructions"]},
                *messages
            ],
            tools=agent_config["tools"] if agent_config["tools"] else None
        )
        
        response_message = response.choices[0].message
        
        # Check for tool calls (handoffs)
        if response_message.tool_calls:
            tool_call = response_message.tool_calls[0]
            function_name = tool_call.function.name
            
            # Execute handoff
            result = available_functions[function_name]()
            
            if "agent" in result:
                print(f"  → Transferring to {agents[result['agent']]['name']}")
                current_agent = result["agent"]
                messages.append({"role": "assistant", "content": f"Transferring you to {agents[current_agent]['name']}..."})
                continue
        
        # No handoff, return final response
        print(f"  Response: {response_message.content}")
        return response_message.content
    
    return "Maximum turns reached"


if __name__ == "__main__":
    try:
        print("=== Sales Query ===")
        run_multi_agent("I want to buy a premium subscription")
        
        print("\n\n=== Support Query ===")
        run_multi_agent("My account is not syncing properly")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires OPENAI_API_KEY.")
