"""
LlamaIndex - RAG Agent Example

Demonstrates a RAG-powered agent that queries documents.
LlamaIndex excels at document ingestion and retrieval.
"""

from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.core.tools import QueryEngineTool, ToolMetadata
from pathlib import Path
import tempfile

# Note: Install with: pip install llama-index llama-index-llms-openai llama-index-embeddings-openai


def create_sample_documents():
    """Create sample documents for demonstration"""
    temp_dir = tempfile.mkdtemp()
    
    # Create sample docs
    doc1 = Path(temp_dir) / "company_policy.txt"
    doc1.write_text("""
    Company Vacation Policy:
    - Employees get 15 days of vacation per year
    - Vacation days accumulate up to 30 days maximum
    - Unused vacation expires at year end
    - Approval required 2 weeks in advance
    """)
    
    doc2 = Path(temp_dir) / "benefits.txt"
    doc2.write_text("""
    Employee Benefits:
    - Health insurance for employee and family
    - 401k matching up to 6%
    - Stock options after 1 year
    - Free gym membership
    - Remote work 3 days per week
    """)
    
    return temp_dir


def run_rag_agent():
    """Run a RAG-powered LlamaIndex agent"""
    try:
        # Configure LLM and embeddings
        Settings.llm = OpenAI(model="gpt-4")
        Settings.embed_model = OpenAIEmbedding()
        
        # Create sample documents
        docs_dir = create_sample_documents()
        
        # Load documents
        documents = SimpleDirectoryReader(docs_dir).load_data()
        
        # Create vector index
        index = VectorStoreIndex.from_documents(documents)
        
        # Create query engine
        query_engine = index.as_query_engine(similarity_top_k=2)
        
        # Wrap query engine as a tool
        query_tool = QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="company_docs",
                description="Useful for answering questions about company policies and benefits"
            )
        )
        
        # Create agent with RAG tool
        agent = ReActAgent.from_tools(
            [query_tool],
            verbose=True
        )
        
        # Query the agent
        questions = [
            "How many vacation days do employees get?",
            "What are the remote work options?",
            "Tell me about the 401k matching"
        ]
        
        for question in questions:
            print(f"\n{'='*60}")
            print(f"Question: {question}")
            print('='*60)
            response = agent.chat(question)
            print(f"Answer: {response}\n")
        
    except Exception as e:
        print(f"Error: {e}")
        print("Note: This example requires 'llama-index' packages and OPENAI_API_KEY.")


if __name__ == "__main__":
    run_rag_agent()
