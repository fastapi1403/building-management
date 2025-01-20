from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.owner import Owner
from app.schemas.owner import OwnerCreate, OwnerUpdate


class CRUDOwner(CRUDBase[Owner, OwnerCreate, OwnerUpdate]):
    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: OwnerCreate,
    ) -> Owner:
        """
        Create a new owner.

        Args:
            db: Database session
            obj_in: Owner creation schema
            created_by: Username of the creator

        Returns:
            Created owner instance
        """
        current_time = datetime.now()
        db_obj = Owner(
            phone=obj_in.phone,
            name=obj_in.name,
            description=obj_in.note,
        )
        return await super().create(db, obj_in=db_obj)

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Owner,
            obj_in: Union[OwnerUpdate, Dict[str, Any]],
    ) -> Owner:
        """
        Update a owner.

        Args:
            db: Database session
            db_obj: Existing owner instance
            obj_in: Update data

        Returns:
            Updated owner instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, OwnerUpdate) else obj_in
        return await super().update(db, db_obj=db_obj, obj_in=obj_data)

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            building_id: Optional[int] = None
    ) -> List[Owner]:
        """
        Get multiple owners with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            building_id: Optional building ID filter

        Returns:
            List of owner instances
        """
        query = select(Owner)
        if building_id:
            query = query.filter(Owner.building_id == building_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(
            self,
            db: AsyncSession,
            *,
            name: str,
            building_id: int
    ) -> Optional[Owner]:
        """
        Get a owner by its name within a building.

        Args:
            db: Database session
            name: Owner name to search for
            building_id: Building ID to scope the search

        Returns:
            Owner instance if found, None otherwise
        """
        query = select(Owner).filter(Owner.name == name, Owner.building_id == building_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_stats(
            self,
            db: AsyncSession,
            building_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get owner statistics.

        Args:
            db: Database session
            building_id: Optional building ID to filter stats

        Returns:
            Dictionary containing owner statistics
        """
        query = select(Owner).filter(Owner.is_deleted == False)
        if building_id:
            query = query.filter(Owner.building_id == building_id)

        result = await db.execute(query)
        owners = result.scalars().all()

        total_units = sum(owner.total_units for owner in owners)
        occupied_units = 0
        for owner in owners:
            occupied_units += await self.get_occupied_units_count(db, owner.id)

        return {
            "total_owners": len(owners),
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": total_units - occupied_units,
            "occupancy_rate": (occupied_units / total_units * 100) if total_units > 0 else 0
        }