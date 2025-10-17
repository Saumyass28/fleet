from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import query_db, init_db, close_db
from config import Config
from agents import create_team
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio

app = FastAPI(title="Industry Monitoring API", version="1.0.0")
config = Config()

# Global team object
team = None

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    response: str
    query: str

@app.on_event("startup")
async def startup_event():
    """Initialize database and agent team on startup"""
    global team
    
    try:
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")
    
    # Initialize agent team
    try:
        llm_client = OpenAIChatCompletionClient(
            model="gpt-4.1",
            api_key=config.OPENAI_API_KEY
        )
        team = create_team(llm_client)
        print("Agent team initialized successfully")
    except Exception as e:
        print(f"Agent team initialization failed: {e}")

@app.on_event("shutdown")
async def shutdown_event():
    """Clean up database connections on shutdown"""
    await close_db()

@app.get("/")
async def root():
    return {"message": "Industry Monitoring API is running"}

@app.get("/query/{query}")
async def query_data(query: str):
    if not query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    try:
        results = await query_db(query)
        return {"results": results, "query": query}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

@app.post("/chat", response_model=QueryResponse)
async def chat_endpoint(request: QueryRequest):
    """Process queries using the agent system"""
    global team
    
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    if not team:
        raise HTTPException(status_code=503, detail="Agent team not initialized")
    
    try:
        final_response = None
        
        # Stream the team workflow
        async for msg in team.run_stream(task=query):
            # Check if FormattingAgentFinal produced output
            if getattr(msg, "source", "") == "FormattingAgentFinal" and getattr(msg, "content", None):
                final_response = msg.content
                break
        
        if final_response:
            return {"response": final_response, "query": query}
        else:
            return {"response": "No response generated from the agent system.", "query": query}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Agent processing error: {str(e)}")

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-09-11"}