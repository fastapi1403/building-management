from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.tenant import Tenant
from app.schemas.tenant import TenantCreate, TenantUpdate


class CRUDTenant(CRUDBase[Tenant, TenantCreate, TenantUpdate]):
    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: TenantCreate,
    ) -> Tenant:
        """
        Create a new tenant.

        Args:
            db: Database session
            obj_in: Tenant creation schema
            created_by: Username of the creator

        Returns:
            Created tenant instance
        """
        current_time = datetime.now()
        db_obj = Tenant(
            phone=obj_in.phone,
            name=obj_in.name,
            description=obj_in.notes,
        )
        return await super().create(db, obj_in=db_obj)

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Tenant,
            obj_in: Union[TenantUpdate, Dict[str, Any]],
    ) -> Tenant:
        """
        Update a tenant.

        Args:
            db: Database session
            db_obj: Existing tenant instance
            obj_in: Update data

        Returns:
            Updated tenant instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, TenantUpdate) else obj_in
        return await super().update(db, db_obj=db_obj, obj_in=obj_data)

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            building_id: Optional[int] = None
    ) -> List[Tenant]:
        """
        Get multiple tenants with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            building_id: Optional building ID filter

        Returns:
            List of tenant instances
        """
        query = select(Tenant)
        if building_id:
            query = query.filter(Tenant.building_id == building_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(
            self,
            db: AsyncSession,
            *,
            name: str,
            building_id: int
    ) -> Optional[Tenant]:
        """
        Get a tenant by its name within a building.

        Args:
            db: Database session
            name: Tenant name to search for
            building_id: Building ID to scope the search

        Returns:
            Tenant instance if found, None otherwise
        """
        query = select(Tenant).filter(Tenant.name == name, Tenant.building_id == building_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_stats(
            self,
            db: AsyncSession,
            building_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get tenant statistics.

        Args:
            db: Database session
            building_id: Optional building ID to filter stats

        Returns:
            Dictionary containing tenant statistics
        """
        query = select(Tenant).filter(Tenant.is_deleted == False)
        if building_id:
            query = query.filter(Tenant.building_id == building_id)

        result = await db.execute(query)
        tenants = result.scalars().all()

        total_units = sum(tenant.total_units for tenant in tenants)
        occupied_units = 0
        for tenant in tenants:
            occupied_units += await self.get_occupied_units_count(db, tenant.id)

        return {
            "total_tenants": len(tenants),
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": total_units - occupied_units,
            "occupancy_rate": (occupied_units / total_units * 100) if total_units > 0 else 0
        }