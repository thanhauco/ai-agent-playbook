from langchain.agents import initialize_agent, Tool
from langchain.agents import AgentType
from langchain.llms import OpenAI

# Note: You need to set OPENAI_API_KEY in your environment variables.

# Mock tools for demonstration purposes as the original code assumed existing tool objects
class MockTool:
    def run(self, query):
        return "This is a mock result for: " + str(query)

calculator = MockTool()
search = MockTool()

llm = OpenAI(temperature=0)

tools = [
    Tool(
        name="Calculator",
        func=calculator.run,
        description="Useful for math calculations"
    ),
    Tool(
        name="Search",
        func=search.run,
        description="Useful for searching the web"
    )
]

agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

agent.run("What's 25% of the GDP of France in 2024?")
