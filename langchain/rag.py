from langchain.vectorstores import Chroma
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
from langchain.llms import OpenAI
from langchain.docstore.document import Document

# Note: You need to set OPENAI_API_KEY in your environment variables.

# Mock documents for demonstration
documents = [
    Document(page_content="Our return policy is 30 days for a full refund.", metadata={"source": "policy"}),
    Document(page_content="Shipping is free for orders over $50.", metadata={"source": "policy"})
]

llm = OpenAI(temperature=0)

# Load documents
# Note: This requires 'chromadb' and 'tiktoken' installed
try:
    vectorstore = Chroma.from_documents(
        documents,
        OpenAIEmbeddings()
    )

    # Create RAG chain
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )

    print(qa.run("What is our return policy?"))
except Exception as e:
    print(f"Error running RAG example (likely missing dependencies or API key): {e}")
