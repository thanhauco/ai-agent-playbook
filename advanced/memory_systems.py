"""
Advanced Memory Systems for Agents (2025)

Demonstrates implementing short-term and long-term memory for agents.
"""

from openai import OpenAI
from datetime import datetime
from typing import List, Dict
import json

client = OpenAI()


class ShortTermMemory:
    """Conversational memory (recent context)"""
    def __init__(self, max_messages: int = 10):
        self.messages: List[Dict] = []
        self.max_messages = max_messages
    
    def add_message(self, role: str, content: str):
        """Add a message to short-term memory"""
        self.messages.append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        
        # Keep only recent messages
        if len(self.messages) > self.max_messages:
            self.messages = self.messages[-self.max_messages:]
    
    def get_messages(self) -> List[Dict]:
        """Get conversation history"""
        return [{"role": m["role"], "content": m["content"]} for m in self.messages]


class LongTermMemory:
    """Persistent memory (facts, preferences, user info)"""
    def __init__(self):
        self.facts: Dict[str, any] = {}
        self.preferences: Dict[str, any] = {}
        self.user_info: Dict[str, any] = {}
    
    def store_fact(self, key: str, value: any):
        """Store a fact"""
        self.facts[key] = {
            "value": value,
            "timestamp": datetime.now().isoformat()
        }
    
    def store_preference(self, key: str, value: any):
        """Store a user preference"""
        self.preferences[key] = value
    
    def store_user_info(self, key: str, value: any):
        """Store user information"""
        self.user_info[key] = value
    
    def get_context(self) -> str:
        """Get long-term memory context for prompt"""
        context_parts = []
        
        if self.user_info:
            context_parts.append(f"User Info: {json.dumps(self.user_info)}")
        
        if self.preferences:
            context_parts.append(f"Preferences: {json.dumps(self.preferences)}")
        
        if self.facts:
            recent_facts = dict(list(self.facts.items())[-5:])  # Last 5 facts
            context_parts.append(f"Recent Facts: {json.dumps({k: v['value'] for k, v in recent_facts.items()})}")
        
        return "\n".join(context_parts) if context_parts else "No stored memory"


class MemoryAgent:
    """Agent with both short-term and long-term memory"""
    def __init__(self):
        self.short_term = ShortTermMemory(max_messages=10)
        self.long_term = LongTermMemory()
    
    def extract_info(self, text: str) -> dict:
        """Extract information to store in long-term memory"""
        # Use LLM to extract key information
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Extract key information from the user's message: "
                        "name, preferences, facts, or other important details. "
                        "Return as JSON with keys: name, preferences, facts."
                    )
                },
                {"role": "user", "content": text}
            ],
            response_format={"type": "json_object"}
        )
        
        return json.loads(response.choices[0].message.content)
    
    def chat(self, user_input: str) -> str:
        """Chat with memory-enabled agent"""
        # Extract and store information
        try:
            extracted = self.extract_info(user_input)
            if extracted.get("name"):
                self.long_term.store_user_info("name", extracted["name"])
            if extracted.get("preferences"):
                for key, value in extracted["preferences"].items():
                    self.long_term.store_preference(key, value)
            if extracted.get("facts"):
                for fact in extracted["facts"]:
                    self.long_term.store_fact(fact, True)
        except:
            pass  # Continue even if extraction fails
        
        # Add to short-term memory
        self.short_term.add_message("user", user_input)
        
        # Build messages with both memory types
        system_prompt = f"""You are a helpful assistant with memory.
        
Long-term Memory:
{self.long_term.get_context()}

Use this information to personalize your responses."""
        
        messages = [{"role": "system", "content": system_prompt}]
        messages.extend(self.short_term.get_messages())
        
        # Get response
        response = client.chat.completions.create(
            model="gpt-4",
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        self.short_term.add_message("assistant", assistant_message)
        
        return assistant_message


def run_memory_demo():
    """Demonstrate memory-enabled agent"""
    agent = MemoryAgent()
    
    conversation = [
        "Hi, I'm Alice and I love Japanese food.",
        "What's my name?",
        "Do you know what kind of food I like?",
        "Recommend a restaurant for me.",
        "I also prefer vegetarian options."
    ]
    
    print("=== Memory-Enabled Agent Demo ===\n")
    
    for user_input in conversation:
        print(f"User: {user_input}")
        response = agent.chat(user_input)
        print(f"Agent: {response}\n")
    
    # Show stored memory
    print("\n=== Stored Long-Term Memory ===")
    print(f"User Info: {agent.long_term.user_info}")
    print(f"Preferences: {agent.long_term.preferences}")
    print(f"Facts: {list(agent.long_term.facts.keys())[:5]}")


if __name__ == "__main__":
    try:
        run_memory_demo()
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Requires OPENAI_API_KEY.")
