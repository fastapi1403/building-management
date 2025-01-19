from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.floor import Floor
from app.schemas.floor import FloorCreate, FloorUpdate


class CRUDFloor(CRUDBase[Floor, FloorCreate, FloorUpdate]):
    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: FloorCreate,
            created_by: str = "fastapi1403"
    ) -> Floor:
        """
        Create a new floor.

        Args:
            db: Database session
            obj_in: Floor creation schema
            created_by: Username of the creator

        Returns:
            Created floor instance
        """
        current_time = datetime.now()
        db_obj = Floor(
            number=obj_in.number,
            name=obj_in.name,
            building_id=obj_in.building_id,
            total_units=obj_in.total_units,
            description=obj_in.description,
        )
        return await super().create(db, obj_in=db_obj)

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Floor,
            obj_in: Union[FloorUpdate, Dict[str, Any]],
    ) -> Floor:
        """
        Update a floor.

        Args:
            db: Database session
            db_obj: Existing floor instance
            obj_in: Update data

        Returns:
            Updated floor instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, FloorUpdate) else obj_in
        return await super().update(db, db_obj=db_obj, obj_in=obj_data)

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            building_id: Optional[int] = None
    ) -> List[Floor]:
        """
        Get multiple floors with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            building_id: Optional building ID filter

        Returns:
            List of floor instances
        """
        query = select(Floor)
        if building_id:
            query = query.filter(Floor.building_id == building_id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(
            self,
            db: AsyncSession,
            *,
            name: str,
            building_id: int
    ) -> Optional[Floor]:
        """
        Get a floor by its name within a building.

        Args:
            db: Database session
            name: Floor name to search for
            building_id: Building ID to scope the search

        Returns:
            Floor instance if found, None otherwise
        """
        query = select(Floor).filter(Floor.name == name, Floor.building_id == building_id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_stats(
            self,
            db: AsyncSession,
            building_id: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Get floor statistics.

        Args:
            db: Database session
            building_id: Optional building ID to filter stats

        Returns:
            Dictionary containing floor statistics
        """
        query = select(Floor).filter(Floor.is_deleted == False)
        if building_id:
            query = query.filter(Floor.building_id == building_id)

        result = await db.execute(query)
        floors = result.scalars().all()

        total_units = sum(floor.total_units for floor in floors)
        occupied_units = 0
        for floor in floors:
            occupied_units += await self.get_occupied_units_count(db, floor.id)

        return {
            "total_floors": len(floors),
            "total_units": total_units,
            "occupied_units": occupied_units,
            "vacant_units": total_units - occupied_units,
            "occupancy_rate": (occupied_units / total_units * 100) if total_units > 0 else 0
        }