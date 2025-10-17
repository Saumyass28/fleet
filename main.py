# main.py

import asyncio
from config import Config
from autogen_ext.models.openai import OpenAIChatCompletionClient
from agents import create_team


async def run_system():
    # Load configuration
    config = Config()

    # Create LLM client (default: OpenAI GPT-4.1)
    llm_client = OpenAIChatCompletionClient(
        model="gpt-4.1",
        api_key=config.OPENAI_API_KEY
    )

    # Build agent team
    team = create_team(llm_client)

    print("\n=== Industry Monitoring System ===")
    print("Ask me about companies or industries.")
    print("Type 'exit' to quit.\n")

    while True:
        user_query = input("Enter your query (or 'exit' to quit): ").strip()
        if user_query.lower() == "exit":
            print("Goodbye!")
            break

        if not user_query:
            print("⚠️ Please enter a valid query.\n")
            continue

        print(f"\nProcessing query: {user_query}")
        print("Agents are working...\n")

        try:
            final_response = None

            # Stream the team workflow
            async for msg in team.run_stream(task=user_query):
                # Print source and message for debugging
                # print(f"[{msg.source}] {getattr(msg, 'content', getattr(msg, 'text', str(msg)))}")

                # Check if FormattingAgentFinal produced output
                if getattr(msg, "source", "") == "FormattingAgentFinal" and getattr(msg, "content", None):
                    final_response = msg.content
                    # Stop the team immediately after the final answer
                    break

            if final_response:
                print("\n=== Final Answer ===")
                print(final_response)
                print("====================\n")
            else:
                print("\n⚠️ No response generated.\n")

        except Exception as e:
            print(f"❌ Error processing query: {e}")


if __name__ == "__main__":
    asyncio.run(run_system())


# #!/usr/bin/env python3
# """
# FastAPI version of the Fleet application with /chat endpoint
# """

# import asyncio
# from fastapi import FastAPI, Request
# from pydantic import BaseModel
# from typing import List
# from config import Config
# from agents import create_team
# from database import init_db, close_db
# from tavily import TavilyClient
# from autogen_ext.models.openai import OpenAIChatCompletionClient

# app = FastAPI()

# # Initialize global team object
# team = None

# class ChatRequest(BaseModel):
#     query: str

# class ChatResponse(BaseModel):
#     messages: List[str]

# @app.on_event("startup")
# async def startup_event():
#     global team
#     config = Config()
#     tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

#     try:
#         await init_db()
#         print("✅ Database initialized")
#     except Exception as e:
#         print(f"❌ Database init failed: {e}")

#     llm_client = OpenAIChatCompletionClient(
#         model="gpt-4.1-nano",
#         api_key=config.OPENAI_API_KEY
#     )

#     team = create_team(llm_client)
#     print("✅ Agent team created")

# @app.on_event("shutdown")
# async def shutdown_event():
#     await close_db()
#     print("🛑 Database connections closed")

# @app.post("/chat", response_model=ChatResponse)
# async def chat_endpoint(request: ChatRequest):
#     query = request.query.strip()
#     if not query:
#         return {"messages": ["⚠️ Empty query received."]}

#     results = []
#     try:
#         async for msg in team.run_stream(task=query):
#             if hasattr(msg, "content") and msg.content and msg.type in ["TextMessage", "ThoughtEvent"] and msg.source == "FormattingAgentFinal":
#                 results.append(msg.content)
#     except Exception as e:
#         return {"messages": [f"❌ Error: {str(e)}"]}

#     return {"messages": results if results else ["⚠️ No relevant messages returned."]}

