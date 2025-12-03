from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator

# Note: You need to have 'langgraph' installed.

class State(TypedDict):
    messages: Annotated[list, operator.add]
    user_query: str
    search_results: list
    final_answer: str

# Mock functions for demonstration
def search_web(state):
    print("Searching web...")
    return {"search_results": ["result1", "result2"]}

def analyze_results(state):
    print("Analyzing results...")
    return {"final_answer": "Analyzed results based on " + str(state["search_results"])}

def generate_response(state):
    print("Generating response...")
    return {"messages": ["Response based on analysis: " + state["final_answer"]]}

# Define graph
workflow = StateGraph(State)

# Add nodes
workflow.add_node("search", search_web)
workflow.add_node("analyze", analyze_results)
workflow.add_node("respond", generate_response)

# Add edges
workflow.add_edge("search", "analyze")
workflow.add_edge("analyze", "respond")
workflow.add_edge("respond", END)

# Set entry point
workflow.set_entry_point("search")

# Compile
app = workflow.compile()

# Run
try:
    result = app.invoke({"user_query": "test", "messages": []})
    print(result)
except Exception as e:
    print(f"Error running LangGraph example: {e}")
