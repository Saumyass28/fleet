# import asyncio
# import sqlalchemy
# from tavily import TavilyClient
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_agentchat.agents import AssistantAgent
# from config import Config
# from agents import create_team
# from database import init_db, store_data, query_db, get_db_session

# async def main():
#     # Initialize configuration and clients
#     config = Config()
#     tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

#     # Initialize database
#     try:
#         await init_db()
#         print("Database connection established")
#     except Exception as e:
#         print(f"Database initialization failed: {e}")
#         print("Please check your database configuration in config.py")
#         return

#     #Create LLM client
#     llm_client = OpenAIChatCompletionClient(
#         model="gpt-4.1",
#         api_key=config.OPENAI_API_KEY
#     )

#     # llm_client = OpenAIChatCompletionClient(
#     #     model="llama-3.2-3b-instruct",
#     #     #model="llama-3.2-3b-instruct@4bit",
#     #     api_key="placeholder",
#     #     base_url="http://127.0.0.1:1234/v1",
#     #     model_info={
#     #         "function_calling": True,
#     #         "json_output": True,
#     #         "vision": False,
#     #         "family": "unknown",
#     #         "structured_output": True
#     #     },
#     # )

#     # Create AutoGen-AgentChat team
#     team = create_team(llm_client)

#     # Main loop for user interaction
#     try:
#         print("\n=== Industry Monitoring System ===")
#         print("Enter your queries to search for company and industry information.")
#         print("The system will search the web, format the data, and store it in the database.")
#         print("Type 'exit' to quit.\n")
        
#         while True:
#             user_query = input("Enter your query (or 'exit' to quit): ")
#             if user_query.lower() == 'exit':
#                 break

#             if not user_query.strip():
#                 print("Please enter a valid query.")
#                 continue

#             print(f"\nProcessing query: {user_query}")
#             print("Agents are working...")

#             try:
#                 # Run the team workflow
#                 async for msg in team.run_stream(task=user_query):
#                     if hasattr(msg, 'content') and msg.content and msg.type in ["TextMessage","ThoughtEvent"] and msg.source == "FormattingAgentFinal":
#                         print(f"\n[{msg.source}]: {msg.content}")
#                     elif hasattr(msg, 'text') and msg.text:
#                         print(f"\n[Agent]: {msg.text}")
#                     # else:
#                     #     print(f"\n[System]: {str(msg)}")
                        
#             except Exception as e:
#                 print(f"Error processing query: {e}")

#     except KeyboardInterrupt:
#         print("\nApplication stopped by user.")
#     except Exception as e:
#         print(f"An error occurred: {e}")
#     finally:
#         # Clean up database connections
#         from database import close_db
#         await close_db()
#         print("Database connections closed.")

# if __name__ == "__main__":
#     asyncio.run(main())


#!/usr/bin/env python3
"""
FastAPI version of the Fleet application with /chat endpoint
"""

import asyncio
from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List
from config import Config
from agents import create_team
from database import init_db, close_db
from tavily import TavilyClient
from autogen_ext.models.openai import OpenAIChatCompletionClient

app = FastAPI()

# Initialize global team object
team = None

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    messages: List[str]

@app.on_event("startup")
async def startup_event():
    global team
    config = Config()
    tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

    try:
        await init_db()
        print("✅ Database initialized")
    except Exception as e:
        print(f"❌ Database init failed: {e}")

    llm_client = OpenAIChatCompletionClient(
        model="gpt-4.1-nano",
        api_key=config.OPENAI_API_KEY
    )

    team = create_team(llm_client)
    print("✅ Agent team created")

@app.on_event("shutdown")
async def shutdown_event():
    await close_db()
    print("🛑 Database connections closed")

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    query = request.query.strip()
    if not query:
        return {"messages": ["⚠️ Empty query received."]}

    results = []
    try:
        async for msg in team.run_stream(task=query):
            if hasattr(msg, "content") and msg.content and msg.type in ["TextMessage", "ThoughtEvent"] and msg.source == "FormattingAgentFinal":
                results.append(msg.content)
    except Exception as e:
        return {"messages": [f"❌ Error: {str(e)}"]}

    return {"messages": results if results else ["⚠️ No relevant messages returned."]}

