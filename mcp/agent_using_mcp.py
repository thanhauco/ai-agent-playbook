from crewai import Agent, Task, Crew
from mcp import MCPClient

# Note: This is a conceptual implementation based on the book's example.

try:
    # Connect to MCP server
    mcp = MCPClient("localhost:8000")
    
    # Create agent
    weather_agent = Agent(
        role="Weather Analyst",
        goal="Provide accurate weather information",
        # Gets all tools from MCP server dynamically
        tools=mcp.get_tools(),
        verbose=True
    )

    # Define a task
    task = Task(
        description="What's the weather in NYC today?",
        agent=weather_agent,
        expected_output="A summary of the current weather in NYC."
    )

    # Create crew
    crew = Crew(
        agents=[weather_agent],
        tasks=[task]
    )

    # Execute
    result = crew.kickoff()
    print(result)

except Exception as e:
    print(f"Error running Agent using MCP: {e}")
    print("Note: This example requires a running MCP server and the 'mcp' library.")
