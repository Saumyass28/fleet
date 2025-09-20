from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, Integer, String, JSON, DateTime, select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import text
from datetime import datetime
from config import Config
import asyncio
import os

Base = declarative_base()

# Global engine and session maker
_engine = None
_async_session = None

class Company(Base):
    __tablename__ = "companies"
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, index=True)
    industry = Column(String(100), index=True)
    data = Column(JSON)
    last_updated = Column(DateTime)

def get_engine():
    global _engine
    if _engine is None:
        # Use SQLite for development (easy setup)
        print("Using SQLite database for development")
        db_path = os.path.join(os.path.dirname(__file__), "industry_monitoring.db")
        _engine = create_async_engine(
            f"sqlite+aiosqlite:///{db_path}",
            echo=False
        )
        print(f"SQLite database path: {db_path}")
    
    return _engine

def get_async_session_maker():
    global _async_session
    if _async_session is None:
        engine = get_engine()
        _async_session = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return _async_session

async def get_db_session():
    session_maker = get_async_session_maker()
    return session_maker()

async def init_db():
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        # SQLite doesn't need explicit index creation if defined in model
        print("Database tables created successfully")
    print("Database initialized successfully")

async def store_data(company_name: str, industry: str, data: dict) -> dict:
    session = await get_db_session()
    try:
        # Check if company exists
        stmt = select(Company).filter_by(name=company_name)
        result = await session.execute(stmt)
        company = result.scalar_one_or_none()
        
        if company:
            company.industry = industry
            company.data = data
            company.last_updated = datetime.now()
            print(f"Updated existing company: {company_name}")
        else:
            company = Company(
                name=company_name,
                industry=industry,
                data=data,
                last_updated=datetime.now()
            )
            session.add(company)
            print(f"Added new company: {company_name}")
        
        await session.commit()
        return {"status": "success", "company": company_name}
    except Exception as e:
        await session.rollback()
        print(f"Database error in store_data: {e}")
        return {"status": "error", "message": str(e)}
    finally:
        await session.close()

async def query_db(query: str) -> dict:
    session = await get_db_session()
    try:
        stmt = select(Company).filter(
            (Company.name.ilike(f"%{query}%")) | (Company.industry.ilike(f"%{query}%"))
        )
        result = await session.execute(stmt)
        companies = result.scalars().all()
        
        if companies:
            print(f"Found {len(companies)} companies matching '{query}'")
            return [{"name": c.name, "industry": c.industry, "data": c.data} for c in companies]
        
        print(f"No companies found matching '{query}'")
        return "No relevant data found."
    except Exception as e:
        print(f"Database query error: {e}")
        return f"Database error: {str(e)}"
    finally:
        await session.close()

async def close_db():
    """Close database connections"""
    global _engine, _async_session
    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session = None
        print("Database connections closed")
