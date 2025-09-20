from tavily import TavilyClient
from config import Config
import asyncio
import httpx

config = Config()
tavily_client = TavilyClient(api_key=config.TAVILY_API_KEY)

async def search_web(query: str) -> dict:
    """Async wrapper for web search using Tavily API"""
    loop = asyncio.get_event_loop()
    # Run the blocking Tavily call in a thread pool
    result = await loop.run_in_executor(
        None, 
        lambda: tavily_client.search(query, max_results=5)
    )
    return result