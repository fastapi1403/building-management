from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.session import get_db

async def get_current_db(db: AsyncSession = Depends(get_db)) -
    try:
        yield db
    finally:
        await db.close()
