from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import Column, Integer, String, JSON, DateTime, select
from sqlalchemy.orm import declarative_base
from datetime import datetime
from config import Config

Base = declarative_base()

# Globals
_engine = None
_async_session = None


class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    industry = Column(String(100), index=True)
    data = Column(JSON)
    last_updated = Column(DateTime, default=datetime.utcnow)


# ---------- Engine / Session Setup ----------

def get_engine():
    """Create global async engine if not already created."""
    global _engine
    if _engine is None:
        config = Config()
        _engine = create_async_engine(
            f"postgresql+asyncpg://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_NAME}",
            echo=False,
            pool_size=10,
            max_overflow=20,
            future=True,
        )
    return _engine


def get_session_maker():
    """Return async session maker bound to engine."""
    global _async_session
    if _async_session is None:
        engine = get_engine()
        _async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
    return _async_session


async def get_db_session() -> AsyncSession:
    """Get a new async session."""
    return get_session_maker()()


# ---------- DB Lifecycle ----------

async def init_db():
    """Create all tables if they don’t exist."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Database initialized and tables ready.")


async def close_db():
    """Dispose engine + reset session maker."""
    global _engine, _async_session
    if _engine:
        await _engine.dispose()
        _engine = None
        _async_session = None
        print("🛑 Database connections closed.")


# ---------- CRUD Operations ----------

async def store_data(company_name: str, industry: str, data: dict) -> dict:
    """Insert or update company record asynchronously, auto-creating table if needed."""
    session_maker = get_session_maker()

    async with session_maker() as session:
        try:
            # Ensure table exists
            engine = get_engine()
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)

            # Check if company exists
            stmt = select(Company).filter_by(name=company_name)
            result = await session.execute(stmt)
            company = result.scalar_one_or_none()

            if company:
                company.industry = industry
                company.data = data
                company.last_updated = datetime.utcnow()
                action = "updated"
            else:
                company = Company(
                    name=company_name,
                    industry=industry,
                    data=data,
                    last_updated=datetime.utcnow(),
                )
                session.add(company)
                action = "inserted"

            await session.commit()
            return {"status": "success", "action": action, "company": company_name}

        except Exception as e:
            await session.rollback()
            return {"status": "error", "message": str(e)}


async def query_db(query: str):
    """Search companies by name or industry (case-insensitive)."""
    session_maker = get_session_maker()

    async with session_maker() as session:
        try:
            stmt = select(Company).filter(
                (Company.name.ilike(f"%{query}%")) | (Company.industry.ilike(f"%{query}%"))
            )
            result = await session.execute(stmt)
            companies = result.scalars().all()

            return [
                {
                    "name": c.name,
                    "industry": c.industry,
                    "data": c.data,
                    "last_updated": c.last_updated.isoformat() if c.last_updated else None,
                }
                for c in companies
            ]

        except Exception as e:
            return {"status": "error", "message": str(e)}