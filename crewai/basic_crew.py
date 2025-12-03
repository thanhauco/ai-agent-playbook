from crewai import Agent, Task, Crew, Process

# Note: You need to set OPENAI_API_KEY in your environment variables.

researcher = Agent(
    role='Market Researcher',
    goal='Uncover cutting-edge developments in AI',
    backstory="""You're an expert market researcher with 10 years
    of experience in the AI industry. You excel at identifying
    trends and opportunities.""",
    verbose=True,
    allow_delegation=False
)
writer = Agent(
    role='Tech Content Writer',
    goal='Craft compelling content about AI advancements',
    backstory="""You're a skilled writer who makes complex
    technical concepts accessible to general audiences.""",
    verbose=True,
    allow_delegation=False
)

research_task = Task(
    description="""Research the latest trends in AI agents,
    focusing on new frameworks and breakthrough applications.
    Identify the top 3 most significant developments.""",
    agent=researcher,
    expected_output="A summary of the top 3 AI agent developments."
)
writing_task = Task(
    description="""Using the research findings, write a 500-word
    article about the future of AI agents. Make it engaging
    and accessible.""",
    agent=writer,
    expected_output="A 500-word article about the future of AI agents."
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, writing_task],
    process=Process.sequential  # or Process.hierarchical
)

result = crew.kickoff()
print(result)
