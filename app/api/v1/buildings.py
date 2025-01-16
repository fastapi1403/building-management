from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.schemas.building import BuildingCreate, BuildingUpdate, BuildingResponse
from app.models.building import Building
from db.session import get_db

router = APIRouter(prefix="/buildings", tags=["buildings"])


@router.get("/", response_model=List[BuildingResponse])
async def read_buildings(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieve buildings.
    """
    buildings = await crud.building.get_multi(db, skip=skip, limit=limit)
    return buildings


@router.post("/", response_model=BuildingResponse)
async def create_building(
        *,
        db: AsyncSession = Depends(get_db),
        building_in: BuildingCreate,
) -> Building:
    """
    Create new building.
    """
    return await crud.building.create(db=db, obj_in=building_in)


@router.get("/{building_id}", response_model=BuildingResponse)
async def read_building(
        building_id: int,
        db: AsyncSession = Depends(get_db)
) -> Building:
    """
    Get building by ID.
    """
    building = await crud.building.get(db=db, id=building_id)
    if not building:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )
    return building


@router.put("/{building_id}", response_model=BuildingResponse)
async def update_building(
        *,
        db: AsyncSession = Depends(get_db),
        building_id: int,
        building_in: BuildingUpdate,
) -> Building:
    """
    Update building.
    """
    building = await crud.building.get(db=db, id=building_id)
    if not building:
        raise HTTPException(
            status_code=404,
            detail="Building not found"
        )
    building = await crud.building.update(
        db=db,
        db_obj=building,
        obj_in=building_in
    )
    return building


@router.delete("/{building_id}", response_model=BuildingResponse)
async def delete_building(
        *,
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

    return await crud.building.delete(db=db, db_obj=building)


@router.post("/{building_id}/restore", response_model=BuildingResponse)
async def restore_building(
        *,
        building_id: int,
        db: AsyncSession = Depends(get_db)
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

    return await crud.building.restore(db=db, db_obj=building)


@router.get("/deleted/", response_model=List[BuildingResponse])
async def get_deleted_buildings(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
) -> List[Building]:
    """
    Retrieve all soft-deleted buildings.
    """
    return await crud.building.get_deleted(db=db, skip=skip, limit=limit)


@router.delete("/{building_id}/permanent", response_model=dict)
async def permanent_delete_building(
        *,
        building_id: int,
        db: AsyncSession = Depends(get_db)
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