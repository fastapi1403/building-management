from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.db.session import get_db
from src.crud import crud_unit
from src.schemas.unit import UnitCreate, UnitUpdate, UnitRead

router = APIRouter()

@router.get("/", response_model=List[UnitRead])
async def get_units(
    db: AsyncSession = Depends(get_db),
    building_id: Optional[int] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    Retrieve units with optional building filter and pagination.
    units = await crud_unit.get_multi(db, building_id=building_id, skip=skip, limit=limit)
    return units
