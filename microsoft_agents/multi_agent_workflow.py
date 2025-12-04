"""
Microsoft Agent Framework - Multi-Agent Workflow Example

Demonstrates multi-agent orchestration combining AutoGen's strengths
with Semantic Kernel's enterprise features.
"""

from azure.ai.agents import Agent, AgentThread, Workflow
from azure.ai.agents.models import MessageRole, HandoffConfig
import os


def create_multi_agent_workflow():
    """Create a multi-agent workflow with handoffs"""
    
    # Research Agent
    researcher = Agent(
        name="Researcher",
        instructions="""You are a research specialist. Gather comprehensive 
        information on topics. When done, handoff to the analyst.""",
        model="gpt-4",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    
    # Analyst Agent
    analyst = Agent(
        name="Analyst",
        instructions="""You are a data analyst. Analyze research findings 
        and identify key insights. When done, handoff to the writer.""",
        model="gpt-4",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    
    # Writer Agent
    writer = Agent(
        name="Writer",
        instructions="""You are a content writer. Create clear, engaging 
        summaries from analysis. This is the final step.""",
        model="gpt-4",
        api_key=os.getenv("AZURE_OPENAI_API_KEY"),
        endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    )
    
    # Configure handoffs
    researcher.handoff_to = [analyst]
    analyst.handoff_to = [writer]
    
    # Create workflow
    workflow = Workflow(
        agents=[researcher, analyst, writer],
        entry_agent=researcher
    )
    
    return workflow


def run_multi_agent_workflow():
    """Run multi-agent workflow"""
    try:
        workflow = create_multi_agent_workflow()
        thread = AgentThread()
        
        # User request
        query = "Research the impact of AI agents on business productivity in 2025"
        print(f"User Request: {query}\n")
        
        thread.add_message(role=MessageRole.USER, content=query)
        
        # Run workflow
        result = workflow.run(thread)
        
        # Display results
        print("\n=== Workflow Execution ===")
        messages = thread.get_messages()
        
        current_agent = None
        for message in messages:
            if message.role == MessageRole.ASSISTANT:
                # Track agent transitions
                agent_name = getattr(message, 'agent_name', 'Unknown')
                if agent_name != current_agent:
                    current_agent = agent_name
                    print(f"\n🤖 [{current_agent}]")
                print(f"  {message.content[:200]}...")
        
        print(f"\n✅ Workflow completed successfully")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires azure-ai-agents and Azure OpenAI credentials.")
        print("\nFallback: Simulating multi-agent workflow...")
        simulate_workflow()


def simulate_workflow():
    """Simulate workflow for demonstration"""
    print("\n=== Simulated Workflow ===")
    print("\n🤖 [Researcher]")
    print("  Gathering information on AI agents and business productivity...")
    print("  ✓ Found 5 key sources")
    
    print("\n🤖 [Analyst]")
    print("  Analyzing research findings...")
    print("  ✓ Identified 3 major productivity improvements: 40% faster response, 60% cost reduction, 24/7 availability")
    
    print("\n🤖 [Writer]")
    print("  Creating final summary...")
    print("  ✓ AI agents in 2025 have transformed business productivity by automating routine tasks,")
    print("    providing instant customer support, and enabling data-driven decision making.")
    
    print("\n✅ Workflow completed")


if __name__ == "__main__":
    print("=== Microsoft Agent Framework - Multi-Agent Workflow ===\n")
    run_multi_agent_workflow()
