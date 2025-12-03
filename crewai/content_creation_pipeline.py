from crewai import Agent, Task, Crew, Process

# Note: You need to set OPENAI_API_KEY in your environment variables.

# Mock tools for demonstration
class MockTool:
    name = "MockTool"
    description = "A mock tool"
    def func(self, query):
        return "Mock result"

search_tool = MockTool()
scrape_tool = MockTool()

# Define agents
researcher = Agent(
    role='Senior Researcher',
    goal='Research AI agent frameworks comprehensively',
    backstory='Expert in AI with 15 years experience',
    tools=[search_tool, scrape_tool],
    verbose=True
)

analyst = Agent(
    role='Data Analyst',
    goal='Analyze research findings and identify patterns',
    backstory='Data scientist specializing in technology trends',
    verbose=True
)

writer = Agent(
    role='Content Writer',
    goal='Create engaging, informative articles',
    backstory='Award-winning tech journalist',
    verbose=True
)

editor = Agent(
    role='Editor',
    goal='Polish content to publication quality',
    backstory='Senior editor with eye for detail',
    verbose=True
)

# Define tasks
research = Task(
    description='Research AI agent frameworks: features, pros, cons',
    agent=researcher,
    expected_output='Comprehensive research report'
)

analysis = Task(
    description='Analyze research and identify top 5 frameworks',
    agent=analyst,
    expected_output='Analytical summary with rankings'
)

writing = Task(
    description='Write 1500-word article from analysis',
    agent=writer,
    expected_output='Draft article'
)

editing = Task(
    description='Edit article for clarity, grammar, flow',
    agent=editor,
    expected_output='Final polished article'
)

# Create crew
crew = Crew(
    agents=[researcher, analyst, writer, editor],
    tasks=[research, analysis, writing, editing],
    process=Process.sequential,
    verbose=True
)

# Execute
result = crew.kickoff()
print(result)
