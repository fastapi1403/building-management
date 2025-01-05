import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from src.main import app
from src.db.base import Base

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
async def test_db():
    test_engine = create_async_engine("sqlite+aiosqlite:///./test.db")
    TestingSessionLocal = sessionmaker(test_engine, class_=AsyncSession)
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield TestingSessionLocal
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
