#!/usr/bin/env python3
"""
Simple test script to verify agent functionality
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def test_agents():
    """Test agent creation and basic functionality"""
    print("=== Testing Agent System ===\n")
    
    try:
        # Test imports
        from database import init_db, store_data
        from tools import search_web
        from formatting_tools import format_web_data
        from config import Config
        
        print("✓ All modules imported successfully")
        
        # Initialize database
        await init_db()
        print("✓ Database initialized")
        
        # Test web search tool
        print("\n--- Testing Web Search ---")
        search_result = await search_web("OpenAI")
        print(f"✓ Web search completed: {len(str(search_result))} characters of data")
        
        # Test formatting tool
        print("\n--- Testing Data Formatting ---")
        formatted_result = await format_web_data(str(search_result))
        print(f"✓ Data formatting completed: {type(formatted_result)}")
        
        # Test data storage
        print("\n--- Testing Data Storage ---")
        if isinstance(formatted_result, dict) and 'company_info' in formatted_result:
            company_name = formatted_result['company_info'].get('name', 'OpenAI')
            industry = formatted_result['company_info'].get('industry', 'Technology')
            store_result = await store_data(company_name, industry, formatted_result)
            print(f"✓ Data storage completed: {store_result}")
        else:
            # Fallback test data
            store_result = await store_data("OpenAI", "Technology", {"test": "data"})
            print(f"✓ Data storage completed (fallback): {store_result}")
        
        print("\n🎉 All agent tools working correctly!")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_agent_creation():
    """Test agent creation (without actually running them)"""
    print("\n=== Testing Agent Creation ===")
    
    try:
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        from agents import create_team
        
        # Create a mock LLM client for testing
        llm_client = OpenAIChatCompletionClient(
            model="gpt-3.5-turbo",
            api_key="test-key",  # This won't be used for creation test
            base_url="http://localhost:1234/v1",  # Mock endpoint
            model_info={
                "function_calling": True,
                "json_output": True,
                "vision": False,
                "family": "openai",
                "structured_output": True
            },
        )
        
        # Create the team
        team = create_team(llm_client)
        print("✓ Agent team created successfully")
        print(f"✓ Team type: {type(team)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Agent creation test failed: {e}")
        return False

if __name__ == "__main__":
    async def run_all_tests():
        print("🚀 Starting Fleet Application Component Tests\n")
        
        # Test basic agent functionality
        tools_ok = await test_agents()
        
        # Test agent creation
        agents_ok = await test_agent_creation()
        
        if tools_ok and agents_ok:
            print("\n✅ All tests passed! The application is ready to run.")
            print("\nYou can now start the application:")
            print("  python3 main.py           # Console application")
            print("  python3 run_app.py web    # Web application")
        else:
            print("\n⚠️  Some tests failed. Please check the errors above.")
    
    try:
        asyncio.run(run_all_tests())
    except KeyboardInterrupt:
        print("\nTests interrupted by user.")
    except Exception as e:
        print(f"Test runner error: {e}")
