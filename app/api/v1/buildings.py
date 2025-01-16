from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from sqlmodel.ext.asyncio.session import AsyncSession

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


@router.delete("/{building_id}", response_model=BuildingResponse)
async def delete_building(
        building_id: int,
        db: AsyncSession = Depends(get_db)
) -> Building:
    """
    Soft delete a building.
    """
    building = await crud.building.get(db=db, id=building_id)
    if not building:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )

    if building.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Building is already deleted"
        )

    return await crud.building.delete(
        db=db,
        db_obj=building
    )


@router.post("/{building_id}/restore", response_model=BuildingResponse)
async def restore_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
) -> Building:
    """
    Restore a soft-deleted building.
    """
    building = await crud.building.get(db=db, id=building_id)
    if not building:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )

    if not building.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Building is not deleted"
        )

    return await crud.building.restore(
        db=db,
        db_obj=building,
    )


@router.get("/deleted/", response_model=List[BuildingResponse])
async def get_deleted_buildings(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db),
) -> List[Building]:
    """
    Retrieve all soft-deleted buildings.
    """
    return await crud.building.get_deleted(
        db=db,
        skip=skip,
        limit=limit
    )


@router.delete("/{building_id}/permanent")
async def permanent_delete_building(
        building_id: int,
        db: AsyncSession = Depends(get_db),
) -> dict:
    """
    Permanently delete a building.
    """
    building = await crud.building.get(db=db, id=building_id)
    if not building:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )

    await crud.building.hard_delete(db=db, db_obj=building)
    return {
        "status": "success",
        "message": f"Building {building_id} has been permanently deleted"
    }