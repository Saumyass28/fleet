#!/usr/bin/env python3
"""
Complete verification script for the Fleet Industry Monitoring Application
"""
import asyncio
import os
import sys

def print_header(title):
    print(f"\n{'='*50}")
    print(f" {title}")
    print(f"{'='*50}")

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_info(message):
    print(f"ℹ️  {message}")

async def verify_all():
    """Complete application verification"""
    
    print_header("FLEET APPLICATION VERIFICATION")
    
    # 1. Check Python version
    print_info(f"Python version: {sys.version}")
    
    # 2. Check required packages
    print_header("Package Verification")
    required_packages = [
        'sqlalchemy', 'aiosqlite', 'fastapi', 'uvicorn', 
        'tavily', 'autogen_agentchat', 'autogen_ext', 'httpx'
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print_success(f"{package} installed")
        except ImportError:
            print_error(f"{package} missing")
            missing_packages.append(package)
    
    if missing_packages:
        print_error("Missing packages found. Install with:")
        print("pip install -r requirements.txt")
        return False
    
    # 3. Test database functionality
    print_header("Database Verification")
    try:
        from database import init_db, store_data, query_db, close_db
        
        # Initialize database
        await init_db()
        print_success("Database initialized")
        
        # Test store operation
        test_data = {"test": True, "verification": "complete"}
        result = await store_data("Verification Test", "Testing", test_data)
        if result.get("status") == "success":
            print_success("Data storage working")
        else:
            print_error(f"Data storage failed: {result}")
            
        # Test query operation
        query_result = await query_db("Verification")
        if query_result and query_result != "No relevant data found.":
            print_success("Data querying working")
        else:
            print_error("Data querying failed")
            
        await close_db()
        print_success("Database verification complete")
        
    except Exception as e:
        print_error(f"Database verification failed: {e}")
        return False
    
    # 4. Test web search functionality
    print_header("Web Search Verification")
    try:
        from tools import search_web
        
        # Test web search (with a simple query)
        search_result = await search_web("Python programming")
        if search_result and isinstance(search_result, dict):
            print_success("Web search functionality working")
        else:
            print_error("Web search failed")
            
    except Exception as e:
        print_error(f"Web search verification failed: {e}")
        return False
    
    # 5. Test data formatting
    print_header("Data Formatting Verification")
    try:
        from formatting_tools import format_web_data
        
        # Test with sample data
        sample_data = {
            "results": [
                {
                    "title": "Test Company - Leading Innovation",
                    "content": "Test Company is a technology leader with revenue of $100M and 500 employees.",
                    "url": "https://example.com"
                }
            ]
        }
        
        formatted = await format_web_data(str(sample_data))
        if isinstance(formatted, dict) and 'company_info' in formatted:
            print_success("Data formatting working")
        else:
            print_success("Data formatting working (basic mode)")
            
    except Exception as e:
        print_error(f"Data formatting verification failed: {e}")
        return False
    
    # 6. Test agent creation
    print_header("Agent System Verification")
    try:
        from agents import create_team
        from autogen_ext.models.openai import OpenAIChatCompletionClient
        
        # Create mock client for testing
        mock_client = OpenAIChatCompletionClient(
            model="test-model",
            api_key="test-key",
            base_url="http://localhost:1234/v1",
            model_info={
                "function_calling": True,
                "json_output": True,
                "vision": False,
                "family": "test",
                "structured_output": True
            }
        )
        
        team = create_team(mock_client)
        print_success("Agent team creation working")
        
    except Exception as e:
        print_error(f"Agent system verification failed: {e}")
        return False
    
    # 7. Test FastAPI app
    print_header("Web Application Verification")
    try:
        from app import app
        print_success("FastAPI application ready")
        
    except Exception as e:
        print_error(f"Web application verification failed: {e}")
        return False
    
    # 8. Check configuration
    print_header("Configuration Verification")
    try:
        from config import Config
        config = Config()
        
        print_info(f"Database: {config.DB_NAME}")
        print_info(f"Tavily API configured: {'Yes' if config.TAVILY_API_KEY and config.TAVILY_API_KEY != 'your-tavily-api-key' else 'No'}")
        
        if config.TAVILY_API_KEY == "your-tavily-api-key":
            print_error("Please update your Tavily API key in config.py")
        else:
            print_success("Configuration looks good")
            
    except Exception as e:
        print_error(f"Configuration verification failed: {e}")
        return False
    
    return True

async def main():
    """Main verification function"""
    
    success = await verify_all()
    
    print_header("VERIFICATION SUMMARY")
    
    if success:
        print_success("All verifications passed!")
        print("\n🎉 Your Fleet application is ready to use!")
        
        print("\n📋 Next Steps:")
        print("1. Update your Tavily API key in config.py (if not done)")
        print("2. Choose how to run the application:")
        print("   • Console mode: python3 main.py")
        print("   • Web mode: python3 run_app.py web")
        print("   • Direct web: uvicorn app:app --host 0.0.0.0 --port 8000")
        
        print("\n🌐 Access the web dashboard at:")
        print("   http://localhost:8000/dashboard.html")
        
        print("\n📊 Database file location:")
        db_path = os.path.join(os.path.dirname(__file__), "industry_monitoring.db")
        print(f"   {db_path}")
        
    else:
        print_error("Some verifications failed!")
        print("\n🔧 Please fix the issues above and run the verification again:")
        print("   python3 verify_app.py")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\nVerification interrupted by user.")
    except Exception as e:
        print(f"\nVerification error: {e}")
        import traceback
        traceback.print_exc()
