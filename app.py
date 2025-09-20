from fastapi import FastAPI, HTTPException
from database import query_db, init_db, close_db
from config import Config
import asyncio

app = FastAPI(title="Industry Monitoring API", version="1.0.0")
config = Config()

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    try:
        await init_db()
        print("Database initialized successfully")
    except Exception as e:
        print(f"Database initialization failed: {e}")

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

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-09-11"}