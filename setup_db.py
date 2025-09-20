#!/usr/bin/env python3
"""
Database setup script for the Fleet application
"""
import asyncio
import sys
import os

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

async def setup_database():
    """Setup the database for the Fleet application"""
    print("=== Fleet Application Database Setup ===\n")
    
    try:
        from config import Config
        config = Config()
        
        print(f"Setting up database: {config.DB_NAME}")
        print(f"Host: {config.DB_HOST}:{config.DB_PORT}")
        print(f"User: {config.DB_USER}")
        
        # Import and run database initialization
        from database import init_db
        await init_db()
        
        print("\n✅ Database setup completed successfully!")
        print("\nYou can now run the application using:")
        print("  python main.py          # Console application")
        print("  python run_app.py web   # Web application")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("\nPlease install required packages:")
        print("  pip install -r requirements.txt")
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        print("\nCommon solutions:")
        print("1. Make sure PostgreSQL is running")
        print("2. Create the database manually:")
        print(f"   createdb {config.DB_NAME}")
        print("3. Check credentials in config.py")
        print("4. Install asyncpg: pip install asyncpg")

if __name__ == "__main__":
    try:
        asyncio.run(setup_database())
    except KeyboardInterrupt:
        print("\nSetup interrupted by user.")
    except Exception as e:
        print(f"Setup error: {e}")
