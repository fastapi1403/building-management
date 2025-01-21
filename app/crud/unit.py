from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate


class CRUDUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):
    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: UnitCreate,
    ) -> Unit:
        """
        Create a new unit.

        Args:
            db: Database session
            obj_in: Unit creation schema
            created_by: Username of the creator

        Returns:
            Created unit instance
        """
        current_time = datetime.now()
        db_obj = Unit(
            phone=obj_in.phone,
            name=obj_in.name,
            description=obj_in.notes,
        )
        return await super().create(db, obj_in=db_obj)

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Unit,
            obj_in: Union[UnitUpdate, Dict[str, Any]],
    ) -> Unit:
        """
        Update a unit.

        Args:
            db: Database session
            db_obj: Existing unit instance
            obj_in: Update data

        Returns:
            Updated unit instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, UnitUpdate) else obj_in
        return await super().update(db, db_obj=db_obj, obj_in=obj_data)

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            building_id: Optional[int] = None
    ) -> List[Unit]:
        """
        Get multiple units with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            building_id: Optional building ID filter

        Returns:
            List of unit instances
        """
        query = select(Unit)
        if building_id:
            query = query.filter(Unit.building_id == building_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(
            self,
            db: AsyncSession,
            *,
            name: str,
            building_id: int
    ) -> Optional[Unit]:
        """
        Get a unit by its name within a building.

        Args:
            db: Database session
            name: Unit name to search for
            building_id: Building ID to scope the search

        Returns:
            Unit instance if found, None otherwise
        """
        query = select(Unit).filter(Unit.name == name, Unit.building_id == building_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_stats(
            self,
            db: AsyncSession,
            building_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get unit statistics.

        Args:
            db: Database session
            building_id: Optional building ID to filter stats

        Returns:
            Dictionary containing unit statistics
        """
        query = select(Unit).filter(Unit.is_deleted == False)
        if building_id:
            query = query.filter(Unit.building_id == building_id)

        result = await db.execute(query)
        units = result.scalars().all()

        total_units = sum(unit.total_units for unit in units)
        occupied_units = 0
        for unit in units:
            occupied_units += await self.get_occupied_units_count(db, unit.id)

        return {
            "total_units": len(units),
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": total_units - occupied_units,
            "occupancy_rate": (occupied_units / total_units * 100) if total_units > 0 else 0
        }