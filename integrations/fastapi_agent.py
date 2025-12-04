"""
Integration: FastAPI Agent Server

REST API for AI agents using FastAPI.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from openai import OpenAI
import uvicorn

app = FastAPI(title="AI Agent API", version="1.0.0")

# Add CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI()


# Request/Response models
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    model: str = "gpt-4"


class ChatResponse(BaseModel):
    response: str
    conversation_id: str


class AgentStatus(BaseModel):
    status: str
    version: str
    models_available: List[str]


# In-memory conversation storage (use Redis in production)
conversations = {}


@app.get("/", response_model=AgentStatus)
async def root():
    """Health check and status"""
    return AgentStatus(
        status="online",
        version="1.0.0",
        models_available=["gpt-4", "gpt-3.5-turbo"]
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Chat with the AI agent"""
    try:
        # Get or create conversation
        conv_id = request.conversation_id or f"conv_{id(request)}"
        messages = conversations.get(conv_id, [])
        
        # Add user message
        messages.append({"role": "user", "content": request.message})
        
        # Call OpenAI
        response = client.chat.completions.create(
            model=request.model,
            messages=messages
        )
        
        assistant_message = response.choices[0].message.content
        messages.append({"role": "assistant", "content": assistant_message})
        
        # Store conversation
        conversations[conv_id] = messages[-10:]  # Keep last 10 messages
        
        return ChatResponse(
            response=assistant_message,
            conversation_id=conv_id
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.delete("/conversation/{conversation_id}")
async def clear_conversation(conversation_id: str):
    """Clear conversation history"""
    if conversation_id in conversations:
        del conversations[conversation_id]
        return {"message": "Conversation cleared"}
    raise HTTPException(status_code=404, detail="Conversation not found")


if __name__ == "__main__":
    print("🚀 Starting AI Agent API Server...")
    print("📖 Docs: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)
