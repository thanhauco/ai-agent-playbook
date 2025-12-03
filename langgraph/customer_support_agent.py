from langgraph.graph import StateGraph, END
from typing import TypedDict, Optional

# Note: You need to have 'langgraph' installed.

# Mock LLM and DB for demonstration
class MockLLM:
    def classify(self, text):
        if "order" in text.lower():
            return "order_issue"
        elif "complex" in text.lower():
            return "complex_issue"
        return "general_response"
llm = MockLLM()

class MockDB:
    def get_customer(self, email):
        return {"last_order_id": "123"}
db = MockDB()

def get_order(order_id):
    return {"status": "shipped"}

def generate_order_response(order, message):
    return f"Order status: {order['status']}"

def create_ticket(state):
    return "TICKET-123"

class SupportState(TypedDict):
    user_message: str
    user_email: str
    conversation_history: list
    customer_data: dict
    ticket_created: bool
    issue_resolved: bool
    intent: Optional[str]
    response: Optional[str]

def classify_intent(state):
    # Classify user intent
    print("Classifying intent...")
    intent = llm.classify(state["user_message"])
    state["intent"] = intent
    return state

def fetch_customer_data(state):
    # Retrieve customer info
    print("Fetching customer data...")
    customer = db.get_customer(state["user_email"])
    state["customer_data"] = customer
    return state

def handle_order_issue(state):
    # Process order-related issues
    print("Handling order issue...")
    order = get_order(state["customer_data"]["last_order_id"])
    response = generate_order_response(order, state["user_message"])
    state["response"] = response
    state["issue_resolved"] = True
    return state

def escalate_to_human(state):
    # Create support ticket
    print("Escalating to human...")
    ticket = create_ticket(state)
    state["ticket_created"] = True
    state["response"] = "I've created a support ticket. A human agent will contact you soon."
    return state

def general_response(state):
    print("Generating general response...")
    state["response"] = "How can I help you?"
    return state

def route_intent(state):
    intent = state.get("intent")
    if intent == "order_issue":
        return "handle_order"
    elif intent == "complex_issue":
        return "escalate"
    else:
        return "general_response"

# Build graph
workflow = StateGraph(SupportState)

workflow.add_node("classify", classify_intent)
workflow.add_node("fetch_data", fetch_customer_data)
workflow.add_node("handle_order", handle_order_issue)
workflow.add_node("escalate", escalate_to_human)
workflow.add_node("general_response", general_response)

workflow.set_entry_point("classify")
workflow.add_edge("classify", "fetch_data")
workflow.add_conditional_edges(
    "fetch_data",
    route_intent,
    {
        "handle_order": "handle_order",
        "escalate": "escalate",
        "general_response": "general_response"
    }
)
workflow.add_edge("handle_order", END)
workflow.add_edge("escalate", END)
workflow.add_edge("general_response", END)

# Compile
app = workflow.compile()

# Run
try:
    print("--- Running Order Issue Test ---")
    result = app.invoke({"user_message": "Where is my order?", "user_email": "test@example.com", "conversation_history": []})
    print("Result:", result)
    
    print("\n--- Running General Query Test ---")
    result = app.invoke({"user_message": "Hello", "user_email": "test@example.com", "conversation_history": []})
    print("Result:", result)
except Exception as e:
    print(f"Error running LangGraph example: {e}")
