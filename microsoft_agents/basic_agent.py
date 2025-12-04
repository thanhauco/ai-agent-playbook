"""
Microsoft Agent Framework - Basic Agent Example

The Microsoft Agent Framework (October 2025) is the unified successor to
Semantic Kernel and AutoGen, combining multi-agent orchestration with
enterprise-grade features.
"""

from azure.ai.agents import Agent, AgentThread
from azure.ai.agents.models import MessageRole
import os

# Note: Install with: pip install azure-ai-agents


def create_basic_agent():
    """Create a simple agent using Microsoft Agent Framework"""
    
    # Initialize agent with system prompt
    agent = Agent(
        name="AssistantAgent",
        instructions="You are a helpful assistant that answers questions clearly and concisely.",
        model="gpt-4",
        # Azure OpenAI configuration
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
       endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    
    return agent


def run_conversation():
    """Run a conversation with the agent"""
    try:
        # Create agent
        agent = create_basic_agent()
        
        # Create thread for state management
        thread = AgentThread()
        
        # Add user message
        thread.add_message(
            role=MessageRole.USER,
            content="What are the key benefits of using AI agents in business?"
        )
        
        # Run agent
        response = agent.run(thread)
        
        # Get response
        messages = thread.get_messages()
        for message in messages:
            if message.role == MessageRole.ASSISTANT:
                print(f"Agent: {message.content}")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires azure-ai-agents and Azure OpenAI credentials.")


if __name__ == "__main__":
    print("=== Microsoft Agent Framework - Basic Example ===\n")
    run_conversation()
