from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate


class CRUDBuilding(CRUDBase[Building, BuildingCreate, BuildingUpdate]):
    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: BuildingCreate,
            created_by: str = "fastapi1403"
    ) -> Building:
        """
        Create a new building.

        Args:
            db: Database session
            obj_in: Building creation schema
            created_by: Username of the creator

        Returns:
            Created building instance
        """
        current_time = datetime.now()
        db_obj = Building(
            name=obj_in.name,
            total_floors=obj_in.total_floors,
            description=obj_in.description,
            created_at=current_time,
            created_by=created_by,
            updated_at=current_time,
            updated_by=created_by,
            is_deleted=False
        )
        # db.add(db_obj)
        # await db.commit()
        # await db.refresh(db_obj)
        # return db_obj
        return await super().create(db, obj_in=db_obj)

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: Building,
            obj_in: Union[BuildingUpdate, Dict[str, Any]],
    ) -> Building:
        """
        Update a building.

        Args:
            db: Database session
            db_obj: Existing building instance
            obj_in: Update data
            updated_by: Username of the updater

        Returns:
            Updated building instance
        """
        obj_data = obj_in.model_dump(exclude_unset=True) if isinstance(obj_in, BuildingUpdate) else obj_in
        return await super().update(db, db_obj=db_obj, obj_in=obj_data)

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100,
            status: Optional[str] = None
    ) -> List[Building]:
        """
        Get multiple buildings with optional filtering.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return
            status: Optional status filter

        Returns:
            List of building instances
        """
        query = select(Building)
        if status:
            query = query.filter(Building.status == status)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_by_name(
            self,
            db: AsyncSession,
            *,
            name: str
    ) -> Optional[Building]:
        """
        Get a building by its name.

        Args:
            db: Database session
            name: Building name to search for

        Returns:
            Building instance if found, None otherwise
        """
        query = select(Building).filter(Building.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_stats(
            self,
            db: AsyncSession
    ) -> Dict[str, Any]:
        """
        Get building statistics.

        Args:
            db: Database session

        Returns:
            Dictionary containing building statistics
        """
        total_query = select(Building).filter(Building.is_deleted == False)
        total_result = await db.execute(total_query)
        total_buildings = len(total_result.scalars().all())

        return {
            "total_buildings": total_buildings,
            "total_units": sum(b.total_units for b in (await self.get_multi(db))),
            "occupied_units": sum(b.occupied_units for b in (await self.get_multi(db)))
        }

    async def delete(
            self,
            db: AsyncSession,
            *,
            db_obj: Building,
            deleted_by: str = "fastapi1403"
    ) -> Building:
        """
        Soft delete a building by setting is_deleted flag and recording deletion metadata.

        Args:
            db: Database session
            db_obj: Building instance to delete
            deleted_by: Username of person performing the deletion

        Returns:
            Updated building instance with deletion flags
        """
        current_time = datetime.now()
        update_data = {
            "is_deleted": True,
            "deleted_at": current_time,
            "updated_at": current_time,
        }

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def restore(
            self,
            db: AsyncSession,
            *,
            db_obj: Building,
            restored_by: str = "fastapi1403"
    ) -> Building:
        """
        Restore a soft-deleted building.

        Args:
            db: Database session
            db_obj: Building instance to restore
            restored_by: Username of person performing the restoration

        Returns:
            Updated building instance with deletion flags removed
        """
        current_time = datetime.now()
        update_data = {
            "is_deleted": False,
            "deleted_at": None,
            "updated_at": current_time
        }

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    from sqlalchemy import and_

    from typing import List
    from sqlalchemy import select

    async def get_deleted(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100
    ) -> List[Building]:
        """
        Get list of soft-deleted buildings.

        Args:
            db: Database session
            skip: Number of records to skip
            limit: Maximum number of records to return

        Returns:
            List of deleted building instances
        """
        query = (
            select(Building)
            .where(Building.is_deleted.is_(True))  # Ensure proper SQLAlchemy filter expression
            .offset(skip)
            .limit(limit)
        )
        result = await db.execute(query)
        return list(result.scalars().all())  # Explicitly convert to list

    async def hard_delete(
            self,
            db: AsyncSession,
            *,
            db_obj: Building
    ) -> None:
        """
        Permanently delete a building from the database.
        WARNING: This operation cannot be undone.

        Args:
            db: Database session
            db_obj: Building instance to permanently delete
        """
        await db.delete(db_obj)
        await db.commit()