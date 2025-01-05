from typing import AsyncGenerator
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from .session import get_db

async def get_async_session() -, None]:
    """Dependency for getting async database session."""
    async for session in get_db():
        yield session

async def commit_and_refresh(session: AsyncSession, obj):
    """Commit changes and refresh object."""
    try:
        session.add(obj)
        await session.commit()
        await session.refresh(obj)
        return obj
    except Exception as e:
        await session.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
