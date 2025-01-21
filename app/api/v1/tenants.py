from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.tenant import TenantCreate, TenantUpdate, TenantResponse
from app.models.tenant import Tenant
from app.crud import crud_tenant, crud_unit
from db.session import get_db

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.get("/", response_model=List[TenantResponse], name="api_v1_read_tenants")
async def read_tenants(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
):
    """
    Retrieve tenants.
    """
    tenants = await crud_tenant.get_multi(db, skip=skip, limit=limit)
    return tenants

@router.post("/", response_model=TenantResponse, name="api_v1_create_tenant")
async def create_tenant(
        *,
        db: AsyncSession = Depends(get_db),
        tenant_in: TenantCreate,
) -> Tenant:
    """
    Create new tenant.
    """
    # First check if the unit exists
    unit = await crud_unit.get(db=db, id=tenant_in.unit_id)
    if not unit:
        raise HTTPException(
            status_code=404,
            detail=f"Unit with id {tenant_in.unit_id} not found"
        )

    # Check if unit already has a tenant
    existing_tenant = await crud_tenant.get_by_unit_id(db=db, unit_id=tenant_in.unit_id)
    if existing_tenant:
        raise HTTPException(
            status_code=400,
            detail=f"Unit {tenant_in.unit_id} is already occupied"
        )
    return await crud_tenant.create(db=db, obj_in=tenant_in)

@router.get("/{tenant_id}", response_model=TenantResponse, name="api_v1_read_tenant")
async def read_tenant(
        tenant_id: int,
        db: AsyncSession = Depends(get_db)
) -> Tenant:
    """
    Get tenant by ID.
    """
    tenant = await crud_tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )
    return tenant

@router.put("/{tenant_id}", response_model=TenantResponse, name="api_v1_update_tenant")
async def update_tenant(
        *,
        db: AsyncSession = Depends(get_db),
        tenant_id: int,
        tenant_in: TenantUpdate,
) -> Tenant:
    """
    Update tenant.
    """
    tenant = await crud_tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )
    tenant = await crud_tenant.update(
        db=db,
        db_obj=tenant,
        obj_in=tenant_in
    )
    return tenant

@router.delete("/{tenant_id}", response_model=TenantResponse, name="api_v1_delete_tenant")
async def delete_tenant(
        *,
        tenant_id: int,
        db: AsyncSession = Depends(get_db)
) -> Tenant:
    """
    Soft delete a tenant.
    """
    tenant = await crud_tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    if tenant.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Tenant is already deleted"
        )

    return await crud_tenant.delete(db=db, db_obj=tenant)

@router.post("/{tenant_id}/restore", response_model=TenantResponse, name="api_v1_restore_tenant")
async def restore_tenant(
        *,
        tenant_id: int,
        db: AsyncSession = Depends(get_db)
) -> Tenant:
    """
    Restore a soft-deleted tenant.
    """
    tenant = await crud_tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    if not tenant.is_deleted:
        raise HTTPException(
            status_code=400,
            detail="Tenant is not deleted"
        )

    return await crud_tenant.restore(db=db, db_obj=tenant)

@router.get("/deleted/", response_model=List[TenantResponse])
async def get_deleted_tenants(
        skip: int = 0,
        limit: int = 100,
        db: AsyncSession = Depends(get_db)
) -> List[Tenant]:
    """
    Retrieve all soft-deleted tenants.
    """
    return await crud_tenant.get_deleted(db=db, skip=skip, limit=limit)

@router.delete("/{tenant_id}/permanent", response_model=dict)
async def permanent_delete_tenant(
        *,
        tenant_id: int,
        db: AsyncSession = Depends(get_db)
) -> dict:
    """
    Permanently delete a tenant.
    """
    tenant = await crud_tenant.get(db=db, id=tenant_id)
    if not tenant:
        raise HTTPException(
            status_code=404,
            detail="Tenant not found"
        )

    await crud_tenant.hard_delete(db=db, db_obj=tenant)
    return {
        "status": "success",
        "message": f"Tenant {tenant_id} has been permanently deleted"
    }