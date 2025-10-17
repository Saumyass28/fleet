#!/usr/bin/env python3
"""
Startup script for the async Fleet application
"""
import asyncio
import uvicorn
from app import app

async def run_main_app():
    """Run the main console application"""
    from main import run_system
    await run_system()

def run_web_app():
    """Run the FastAPI web application"""
    uvicorn.run(app, host="0.0.0.0", port=8000)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "console":
        print("Starting console application...")
        asyncio.run(run_main_app())
    else:
        print("Starting web application...")
        run_web_app()
