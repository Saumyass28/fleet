#!/usr/bin/env python3
"""
Test script to verify database connection and basic functionality
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database import init_db, store_data, query_db, close_db
from config import Config

async def test_database():
    """Test database connectivity and basic operations"""
    print("Testing database connection...")
    
    try:
        # Test 1: Initialize database
        print("1. Initializing database...")
        await init_db()
        print("✓ Database initialized successfully")
        
        # Test 2: Store test data
        print("2. Storing test data...")
        test_data = {
            "description": "Test company for verification",
            "revenue": "$1B",
            "employees": "1000"
        }
        result = await store_data("Test Company", "Technology", test_data)
        print(f"✓ Data stored: {result}")
        
        # Test 3: Query data
        print("3. Querying data...")
        results = await query_db("Test Company")
        print(f"✓ Query results: {results}")
        
        # Test 4: Search by industry
        print("4. Searching by industry...")
        results = await query_db("Technology")
        print(f"✓ Industry search results: {results}")
        
        print("\n✅ All database tests passed!")
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        print("\nPossible issues:")
        print("1. PostgreSQL is not running")
        print("2. Database credentials in config.py are incorrect")
        print("3. Database 'industry_monitoring' doesn't exist")
        print("4. Required Python packages are not installed")
        return False
    
    finally:
        await close_db()
    
    return True

async def test_config():
    """Test configuration loading"""
    print("Testing configuration...")
    try:
        config = Config()
        print(f"✓ Database: {config.DB_NAME}")
        print(f"✓ Host: {config.DB_HOST}:{config.DB_PORT}")
        print(f"✓ User: {config.DB_USER}")
        print(f"✓ Tavily API configured: {'Yes' if config.TAVILY_API_KEY else 'No'}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    print("=== Fleet Application Database Test ===\n")
    
    async def run_tests():
        # Test configuration first
        config_ok = await test_config()
        if not config_ok:
            return
        
        print()
        # Test database
        db_ok = await test_database()
        
        if db_ok:
            print("\n🎉 All tests passed! Your application should work correctly.")
        else:
            print("\n⚠️  Some tests failed. Please fix the issues before running the application.")
    
    try:
        asyncio.run(run_tests())
    except KeyboardInterrupt:
        print("\nTest interrupted by user.")
    except Exception as e:
        print(f"Test runner error: {e}")
