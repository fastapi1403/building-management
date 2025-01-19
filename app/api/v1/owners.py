from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.owner import OwnerCreate, OwnerUpdate, OwnerResponse
from app.models.owner import Owner
from app.crud import crud_owner
from db.session import get_db

router = APIRouter(prefix="/owners", tags=["owners"])

@router.get("/", response_model=List[OwnerResponse], name="api_v1_read_owners")
async def read_owners(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieve owners.
    """
    owners = await crud_owner.get_multi(db, skip=skip, limit=limit)
    return owners

@router.post("/", response_model=OwnerResponse, name="api_v1_create_owner")
async def create_owner(
        *,
        db: AsyncSession = Depends(get_db),
        owner_in: OwnerCreate,
) -> Owner:
    """
    Create new owner.
    """
    return await crud_owner.create(db=db, obj_in=owner_in)

@router.get("/{owner_id}", response_model=OwnerResponse, name="api_v1_read_owner")
async def read_owner(
        owner_id: int,
        db: AsyncSession = Depends(get_db)
) -> Owner:
    """
    Get owner by ID.
    """
    owner = await crud_owner.get(db=db, id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )
    return owner

@router.put("/{owner_id}", response_model=OwnerResponse, name="api_v1_update_owner")
async def update_owner(
        *,
        db: AsyncSession = Depends(get_db),
        owner_id: int,
        owner_in: OwnerUpdate,
) -> Owner:
    """
    Update owner.
    """
    owner = await crud_owner.get(db=db, id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )
    owner = await crud_owner.update(
        db=db,
        db_obj=owner,
        obj_in=owner_in
    )
    return owner

@router.delete("/{owner_id}", response_model=OwnerResponse, name="api_v1_delete_owner")
async def delete_owner(
        *,
        owner_id: int,
        db: AsyncSession = Depends(get_db)
) -> Owner:
    """
    Soft delete a owner.
    """
    owner = await crud_owner.get(db=db, id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    if owner.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Owner is already deleted"
        )

    return await crud_owner.delete(db=db, db_obj=owner)

@router.post("/{owner_id}/restore", response_model=OwnerResponse, name="api_v1_restore_owner")
async def restore_owner(
        *,
        owner_id: int,
        db: AsyncSession = Depends(get_db)
) -> Owner:
    """
    Restore a soft-deleted owner.
    """
    owner = await crud_owner.get(db=db, id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    if not owner.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Owner is not deleted"
        )

    return await crud_owner.restore(db=db, db_obj=owner)

@router.get("/deleted/", response_model=List[OwnerResponse])
async def get_deleted_owners(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
) -> List[Owner]:
    """
    Retrieve all soft-deleted owners.
    """
    return await crud_owner.get_deleted(db=db, skip=skip, limit=limit)

@router.delete("/{owner_id}/permanent", response_model=dict)
async def permanent_delete_owner(
        *,
        owner_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Permanently delete a owner.
    """
    owner = await crud_owner.get(db=db, id=owner_id)
    if not owner:
        raise HTTPException(
            status_code=404,
            detail="Owner not found"
        )

    await crud_owner.hard_delete(db=db, db_obj=owner)
    return {
        "status": "success",
        "message": f"Owner {owner_id} has been permanently deleted"
    }