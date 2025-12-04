"""
Real-World Use Case: Research Assistant

An AI research assistant that:
- Searches for information (simulated)
- Summarizes findings
- Generates comprehensive reports
- Uses RAG for document analysis
"""

from openai import OpenAI
from typing import List, Dict
import json

client = OpenAI()


def web_search(query: str, num_results: int = 5) -> str:
    """Simulate web search (in production, use real search API)"""
    # Mock search results
    results = [
        {
            "title": f"Result for '{query}' - Article {i+1}",
            "url": f"https://example.com/article-{i+1}",
            "snippet": f"This article discusses {query} with insights on recent developments..."
        }
        for i in range(num_results)
    ]
    return json.dumps({"query": query, "results": results, "total": num_results})


def summarize_text(text: str, max_sentences: int = 3) -> str:
    """Summarize long text"""
    # In production, this would use actual summarization
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": f"Summarize this text in {max_sentences} sentences."},
            {"role": "user", "content": text}
        ]
    )
    return response.choices[0].message.content


def save_report(title: str, content: str) -> str:
    """Save research report"""
    filename = title.lower().replace(" ", "_") + ".md"
    return json.dumps({
        "saved": True,
        "filename": filename,
        "message": f"Report saved as {filename}"
    })


tools = [
    {
        "type": "function",
        "function": {
            "name": "web_search",
            "description": "Search the web for information",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {"type": "string"},
                    "num_results": {"type": "integer", "minimum": 1, "maximum": 10}
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "save_report",
            "description": "Save research report to file",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "content": {"type": "string"}
                },
                "required": ["title", "content"]
            }
        }
    }
]

available_functions = {
    "web_search": web_search,
    "save_report": save_report
}


class ResearchAssistant:
    """AI Research Assistant with multi-step workflow"""
    
    def __init__(self):
        self.system_prompt = """You are an AI research assistant. 

Your workflow:
1. Search for information using web_search
2. Analyze and synthesize findings
3. Generate comprehensive reports
4. Save reports using save_report

Be thorough, cite sources, and provide actionable insights."""
    
    def research(self, topic: str) -> str:
        """Conduct research on a topic"""
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": f"Research this topic and create a report: {topic}"}
        ]
        
        print(f"🔍 Researching: {topic}\n")
        
        # Iterative agent loop
        for iteration in range(5):  # Max 5 iterations
            response = client.chat.completions.create(
                model="gpt-4",
                messages=messages,
                tools=tools
            )
            
            response_message = response.choices[0].message
            
            # Check if done
            if not response_message.tool_calls:
                print("✅ Research complete\n")
                return response_message.content
            
            # Execute tools
            messages.append(response_message)
            
            for tool_call in response_message.tool_calls:
                function_name = tool_call.function.name
                function_args = json.loads(tool_call.function.arguments)
                
                print(f"🔧 Using tool: {function_name}({function_args})")
                
                function_response = available_functions[function_name](**function_args)
                
                messages.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": function_name,
                    "content": function_response
                })
        
        return "Research workflow completed (max iterations reached)"


def demo():
    """Demo the research assistant"""
    assistant = ResearchAssistant()
    
    topics = [
        "Latest developments in AI agents for business automation",
        "Best practices for deploying LLM-based applications"
    ]
    
    print("=== Research Assistant Demo ===\n")
    
    for topic in topics:
        print("=" * 70)
        result = assistant.research(topic)
        print(f"\n📄 Report:\n{result}\n")
        print("=" * 70 + "\n")


if __name__ == "__main__":
    try:
        demo()
    except Exception as e:
        print(f"Error: {e}")
        print("Note: Requires OPENAI_API_KEY.")
