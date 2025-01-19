from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.floor import FloorCreate, FloorUpdate, FloorResponse
from app.models.floor import Floor
from app.crud import crud_floor
from db.session import get_db

router = APIRouter(prefix="/floors", tags=["floors"])

@router.get("/", response_model=List[FloorResponse], name="api_v1_read_floors")
async def read_floors(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieve floors.
    """
    floors = await crud_floor.get_multi(db, skip=skip, limit=limit)
    return floors

@router.post("/", response_model=FloorResponse, name="api_v1_create_floor")
async def create_floor(
        *,
        db: AsyncSession = Depends(get_db),
        floor_in: FloorCreate,
) -> Floor:
    """
    Create new floor.
    """
    return await crud_floor.create(db=db, obj_in=floor_in)

@router.get("/{floor_id}", response_model=FloorResponse, name="api_v1_read_floor")
async def read_floor(
        floor_id: int,
        db: AsyncSession = Depends(get_db)
) -> Floor:
    """
    Get floor by ID.
    """
    floor = await crud_floor.get(db=db, id=floor_id)
    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )
    return floor

@router.put("/{floor_id}", response_model=FloorResponse, name="api_v1_update_floor")
async def update_floor(
        *,
        db: AsyncSession = Depends(get_db),
        floor_id: int,
        floor_in: FloorUpdate,
) -> Floor:
    """
    Update floor.
    """
    floor = await crud_floor.get(db=db, id=floor_id)
    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )
    floor = await crud_floor.update(
        db=db,
        db_obj=floor,
        obj_in=floor_in
    )
    return floor

@router.delete("/{floor_id}", response_model=FloorResponse, name="api_v1_delete_floor")
async def delete_floor(
        *,
        floor_id: int,
        db: AsyncSession = Depends(get_db)
) -> Floor:
    """
    Soft delete a floor.
    """
    floor = await crud_floor.get(db=db, id=floor_id)
    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )

    if floor.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Floor is already deleted"
        )

    return await crud_floor.delete(db=db, db_obj=floor)

@router.post("/{floor_id}/restore", response_model=FloorResponse, name="api_v1_restore_floor")
async def restore_floor(
        *,
        floor_id: int,
        db: AsyncSession = Depends(get_db)
) -> Floor:
    """
    Restore a soft-deleted floor.
    """
    floor = await crud_floor.get(db=db, id=floor_id)
    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )

    if not floor.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Floor is not deleted"
        )

    return await crud_floor.restore(db=db, db_obj=floor)

@router.get("/deleted/", response_model=List[FloorResponse])
async def get_deleted_floors(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
) -> List[Floor]:
    """
    Retrieve all soft-deleted floors.
    """
    return await crud_floor.get_deleted(db=db, skip=skip, limit=limit)

@router.delete("/{floor_id}/permanent", response_model=dict)
async def permanent_delete_floor(
        *,
        floor_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Permanently delete a floor.
    """
    floor = await crud_floor.get(db=db, id=floor_id)
    if not floor:
        raise HTTPException(
            status_code=404,
            detail="Floor not found"
        )

    await crud_floor.hard_delete(db=db, db_obj=floor)
    return {
        "status": "success",
        "message": f"Floor {floor_id} has been permanently deleted"
    }