from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_db
from app.crud import unit as crud
from app.schemas.unit import UnitResponse, UnitCreate, UnitUpdate

router = APIRouter()

@router.get("/units/", response_model=List[UnitResponse])
async def read_units(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    units = await crud.get_units(db, skip=skip, limit=limit)
    return units


@router.post("/units/", response_model=UnitResponse)
async def create_unit(
    unit: UnitCreate,
    db: Session = Depends(get_db)
):
    return await crud.create_unit(db, unit)


@router.get("/units/{unit_id}", response_model=UnitResponse)
async def read_unit(
    unit_id: int,
    db: Session = Depends(get_db)
):
    unit = await crud.get_unit(db, unit_id)
    if unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return unit


@router.put("/units/{unit_id}", response_model=UnitResponse)
async def update_unit(
    unit_id: int,
    unit: UnitUpdate,
    db: Session = Depends(get_db)
):
    updated_unit = await crud.update_unit(db, unit_id, unit)
    if updated_unit is None:
        raise HTTPException(status_code=404, detail="Unit not found")
    return updated_unit


@router.delete("/units/{unit_id}")
async def delete_unit(
    unit_id: int,
    db: Session = Depends(get_db)
):
    deleted = await crud.delete_unit(db, unit_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Unit not found")
    return {"message": "Unit deleted successfully"}