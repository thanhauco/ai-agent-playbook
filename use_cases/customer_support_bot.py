"""
Real-World Use Case: Customer Support Bot

A production-ready customer support agent that:
- Answers FAQs using RAG
- Creates support tickets
- Escalates to human agents when needed
- Maintains conversation context
"""

from openai import OpenAI
from typing import Dict, List, Optional
import json
from datetime import datetime

client = OpenAI()


# Mock knowledge base
FAQ_DATABASE = {
    "refund_policy": "Refunds are available within 30 days of purchase. Contact support@example.com.",
    "shipping": "Standard shipping takes 5-7 business days. Express shipping is 2-3 days.",
    "account_issues": "To reset your password, click 'Forgot Password' on the login page.",
    "pricing": "We offer Basic ($9/mo), Pro ($29/mo), and Enterprise (custom) plans.",
    "cancel_subscription": "You can cancel anytime from your account settings. No cancellation fees."
}


def search_faq(query: str) -> str:
    """Search FAQ database (simplified RAG simulation)"""
    query_lower = query.lower()
    
    for topic, answer in FAQ_DATABASE.items():
        if topic.replace("_", " ") in query_lower or any(word in query_lower for word in topic.split("_")):
            return json.dumps({"topic": topic, "answer": answer})
    
    return json.dumps({"topic": "not_found", "answer": "No matching FAQ found"})


def create_ticket(category: str, description: str, priority: str = "medium") -> str:
    """Create a support ticket"""
    ticket_id = f"TICKET-{int(datetime.now().timestamp())}"
    return json.dumps({
        "ticket_id": ticket_id,
        "category": category,
        "description": description,
        "priority": priority,
        "status": "open",
        "created_at": datetime.now().isoformat()
    })


def escalate_to_human(reason: str) -> str:
    """Escalate conversation to human agent"""
    return json.dumps({
        "escalated": True,
        "reason": reason,
        "estimated_wait": "5-10 minutes",
        "message": "Connecting you with a human agent..."
    })


# Tool definitions
tools = [
    {
        "type": "function",
        "function": {
            "name": "search_faq",
            "description": "Search the FAQ database for answers to common questions",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "create_ticket",
            "description": "Create a support ticket for complex issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "category": {"type": "string", "description": "Issue category"},
                    "description": {"type": "string", "description": "Detailed description"},
                    "priority": {"type": "string", "enum": ["low", "medium", "high", "urgent"]}
                },
                "required": ["category", "description"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "escalate_to_human",
            "description": "Escalate to human agent for complex or sensitive issues",
            "parameters": {
                "type": "object",
                "properties": {
                    "reason": {"type": "string", "description": "Reason for escalation"}
                },
                "required": ["reason"]
            }
        }
    }
]

available_functions = {
    "search_faq": search_faq,
    "create_ticket": create_ticket,
    "escalate_to_human": escalate_to_human
}


class CustomerSupportBot:
    """Customer support bot with context management"""
    
    def __init__(self):
        self.conversation_history: List[Dict] = []
        self.system_prompt = """You are a helpful customer support agent. 

Instructions:
- Be friendly, professional, and empathetic
- Use search_faq for common questions
- Create tickets for technical issues or bugs
- Escalate to humans for billing disputes or complaints
- Always provide clear, concise answers
"""
    
    def chat(self, user_message: str) -> str:
        """Process user message and return response"""
        self.conversation_history.append({
            "role": "user",
            "content": user_message
        })
        
        messages = [{"role": "system", "content": self.system_prompt}]
        messages.extend(self.conversation_history)
        
        # First API call
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages,
            tools=tools
        )
        
        response_message = response.choices[0].message
        
        # Handle tool calls
        if response_message.tool_calls:
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                # Execute function
                function_response = available_functions[function_name](**function_args)
                
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
            
            assistant_message = final_response.choices[0].message.content
        else:
            assistant_message = response_message.content
        
        self.conversation_history.append({
            "role": "assistant",
            "content": assistant_message
        })
        
        return assistant_message


def demo():
    """Demo the customer support bot"""
    bot = CustomerSupportBot()
    
    test_queries = [
        "What's your refund policy?",
        "My account login is broken and I've tried everything",
        "I was charged twice for my subscription!"
    ]
    
    print("=== Customer Support Bot Demo ===\n")
    
    for query in test_queries:
        print(f"User: {query}")
        response = bot.chat(query)
        print(f"Bot: {response}\n")
        print("-" * 60 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Requires OPENAI_API_KEY environment variable.")
