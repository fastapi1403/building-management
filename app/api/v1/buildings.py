from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_db
from app.crud import building as crud
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse

router = APIRouter()

@router.get("/buildings/", response_model=List[BuildingResponse])
async def read_buildings(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    buildings = await crud.get_buildings(db, skip=skip, limit=limit)
    return buildings


@router.post("/buildings/", response_model=BuildingResponse)
async def create_building(
    building: BuildingCreate,
    db: Session = Depends(get_db)
):
    return await crud.create_building(db, building)


@router.get("/buildings/{building_id}", response_model=BuildingResponse)
async def read_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    building = await crud.get_building(db, building_id)
    if building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return building


@router.put("/buildings/{building_id}", response_model=BuildingResponse)
async def update_building(
    building_id: int,
    building: BuildingUpdate,
    db: Session = Depends(get_db)
):
    updated_building = await crud.update_building(
        db, building_id, building
    )
    if updated_building is None:
        raise HTTPException(status_code=404, detail="Building not found")
    return updated_building


@router.delete("/buildings/{building_id}")
async def delete_building(
    building_id: int,
    db: Session = Depends(get_db)
):
    deleted = await crud.delete_building(db, building_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Building not found")
    return {"message": "Building deleted successfully"}
