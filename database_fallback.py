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
        config = Config()
        
        # Try PostgreSQL first, fallback to SQLite
        try:
            # PostgreSQL connection
            _engine = create_async_engine(
                f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}",
                echo=False,
                pool_size=10,
                max_overflow=20
            )
            print("Using PostgreSQL database")
        except Exception as e:
            print(f"PostgreSQL not available ({e}), falling back to SQLite")
            # SQLite fallback
            db_path = os.path.join(os.path.dirname(__file__), "industry_monitoring.db")
            _engine = create_async_engine(
                f"sqlite+aiosqlite:///{db_path}",
                echo=False
            )
            print(f"Using SQLite database: {db_path}")
    
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
        # Create indexes explicitly if not handled by SQLAlchemy
        try:
            await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_company_name ON companies(name);"))
            await conn.execute(text("CREATE INDEX IF NOT EXISTS idx_industry ON companies(industry);"))
        except Exception as e:
            print(f"Index creation info: {e}")
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
        else:
            company = Company(
                name=company_name,
                industry=industry,
                data=data,
                last_updated=datetime.now()
            )
            session.add(company)
        
        await session.commit()
        return {"status": "success", "company": company_name}
    except Exception as e:
        await session.rollback()
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
            return [{"name": c.name, "industry": c.industry, "data": c.data} for c in companies]
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
