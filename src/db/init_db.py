import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.config import settings
from .session import engine, SessionLocal
from .base import Base

async def init_db() -
    """Initialize database."""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_session() -
    """Get database session."""
    async with SessionLocal() as session:
        yield session

if __name__ == "__main__":
    asyncio.run(init_db())
