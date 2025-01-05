from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.db.session import get_db
from src.crud import crud_building
from src.schemas.building import BuildingCreate, BuildingUpdate, BuildingRead

router = APIRouter()

@router.get("/", response_model=List[BuildingRead])
async def get_buildings(
    db: AsyncSession = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    Retrieve buildings with pagination.
    buildings = await crud_building.get_multi(db, skip=skip, limit=limit)
    return buildings
