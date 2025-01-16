from typing import List, Optional, Union, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, or_
from sqlalchemy.sql import func
from datetime import datetime, UTC

from app.models.building import Building
from app.schemas.building import BuildingCreate, BuildingUpdate
from app.core.logging import logger
from app.core.exceptions import (
    # BuildingNotFoundException,
    # BuildingAlreadyExistsException,
    DatabaseOperationException
)


class BuildingCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session
        self.model = Building

    async def create(self, building_data: BuildingCreate) -> Building:
        """
        Create a new building.

        Args:
            building_data: BuildingCreate schema with building information

        Returns:
            Building: Created building instance

        Raises:
            BuildingAlreadyExistsException: If building with same name exists
            DatabaseOperationException: For any other database errors
        """
        try:
            # Check if building with same name exists
            existing_building = await self.get_by_name(building_data.name)
            if existing_building:
                logger.warning(f"Attempted to create duplicate building with name: {building_data.name}")
                raise BuildingAlreadyExistsException(
                    f"Building with name '{building_data.name}' already exists"
                )

            # Create new building instance
            building = Building(**building_data.model_dump())
            self.db.add(building)
            await self.db.commit()
            await self.db.refresh(building)

            logger.info(f"Created new building with ID: {building.id}")
            return building

        except Exception as e:
            logger.error(f"Error creating building: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(f"Failed to create building: {str(e)}")

    async def get(self, building_id: int) -> Optional[Building]:
        """
        Get building by ID.

        Args:
            building_id: ID of the building to retrieve

        Returns:
            Optional[Building]: Building instance if found, None otherwise

        Raises:
            BuildingNotFoundException: If building doesn't exist
        """
        try:
            query = select(self.model).where(
                and_(
                    self.model.id == building_id,
                    self.model.deleted_at.is_(None)
                )
            )
            result = await self.db.execute(query)
            building = result.scalar_one_or_none()

            if not building:
                logger.warning(f"Building not found with ID: {building_id}")
                raise BuildingNotFoundException(f"Building with ID {building_id} not found")

            return building

        except BuildingNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error retrieving building {building_id}: {str(e)}")
            raise DatabaseOperationException(f"Failed to retrieve building: {str(e)}")

    async def get_by_name(self, name: str) -> Optional[Building]:
        """Get building by name."""
        try:
            query = select(self.model).where(
                and_(
                    func.lower(self.model.name) == name.lower(),
                    self.model.deleted_at.is_(None)
                )
            )
            result = await self.db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            logger.error(f"Error retrieving building by name '{name}': {str(e)}")
            raise DatabaseOperationException(f"Failed to retrieve building by name: {str(e)}")

    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Building]:
        """
        Get multiple buildings with filtering options.

        Args:
            skip: Number of records to skip
            limit: Maximum number of records to return
            filters: Dictionary of filter parameters

        Returns:
            List[Building]: List of building instances
        """
        try:
            query = select(self.model).where(self.model.deleted_at.is_(None))

            # Apply filters if provided
            if filters:
                if filters.get("city"):
                    query = query.where(self.model.city == filters["city"])
                if filters.get("total_floors_gt"):
                    query = query.where(self.model.total_floors > filters["total_floors_gt"])
                if filters.get("search"):
                    search_term = f"%{filters['search']}%"
                    query = query.where(
                        or_(
                            self.model.name.ilike(search_term),
                            self.model.address.ilike(search_term),
                            self.model.city.ilike(search_term)
                        )
                    )

            query = query.offset(skip).limit(limit)
            result = await self.db.execute(query)
            return result.scalars().all()

        except Exception as e:
            logger.error(f"Error retrieving buildings list: {str(e)}")
            raise DatabaseOperationException(f"Failed to retrieve buildings: {str(e)}")

    async def update(
            self,
            building_id: int,
            building_data: BuildingUpdate
    ) -> Building:
        """
        Update building information.

        Args:
            building_id: ID of building to update
            building_data: BuildingUpdate schema with update data

        Returns:
            Building: Updated building instance

        Raises:
            BuildingNotFoundException: If building doesn't exist
        """
        try:
            building = await self.get(building_id)
            if not building:
                raise BuildingNotFoundException(f"Building with ID {building_id} not found")

            update_data = building_data.model_dump(exclude_unset=True)

            if update_data:
                update_data["updated_at"] = datetime.now(UTC)
                query = (
                    update(self.model)
                    .where(self.model.id == building_id)
                    .values(update_data)
                    .returning(self.model)
                )
                result = await self.db.execute(query)
                await self.db.commit()

                updated_building = result.scalar_one()
                logger.info(f"Updated building ID: {building_id}")
                return updated_building

            return building

        except BuildingNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error updating building {building_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(f"Failed to update building: {str(e)}")

    async def delete(self, building_id: int) -> bool:
        """
        Soft delete building.

        Args:
            building_id: ID of building to delete

        Returns:
            bool: True if successful

        Raises:
            BuildingNotFoundException: If building doesn't exist
        """
        try:
            building = await self.get(building_id)
            if not building:
                raise BuildingNotFoundException(f"Building with ID {building_id} not found")

            # Soft delete - update deleted_at timestamp
            query = (
                update(self.model)
                .where(self.model.id == building_id)
                .values(deleted_at=datetime.now(UTC))
            )
            await self.db.execute(query)
            await self.db.commit()

            logger.info(f"Soft deleted building ID: {building_id}")
            return True

        except BuildingNotFoundException:
            raise
        except Exception as e:
            logger.error(f"Error deleting building {building_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(f"Failed to delete building: {str(e)}")

    async def hard_delete(self, building_id: int) -> bool:
        """
        Permanently delete building (use with caution).

        Args:
            building_id: ID of building to permanently delete

        Returns:
            bool: True if successful
        """
        try:
            query = delete(self.model).where(self.model.id == building_id)
            result = await self.db.execute(query)
            await self.db.commit()

            if result.rowcount > 0:
                logger.warning(f"Permanently deleted building ID: {building_id}")
                return True

            logger.warning(f"Attempted to hard delete non-existent building ID: {building_id}")
            return False

        except Exception as e:
            logger.error(f"Error permanently deleting building {building_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(f"Failed to permanently delete building: {str(e)}")

    async def restore(self, building_id: int) -> Building:
        """
        Restore a soft-deleted building.

        Args:
            building_id: ID of building to restore

        Returns:
            Building: Restored building instance
        """
        try:
            query = (
                update(self.model)
                .where(
                    and_(
                        self.model.id == building_id,
                        self.model.deleted_at.isnot(None)
                    )
                )
                .values(deleted_at=None)
                .returning(self.model)
            )
            result = await self.db.execute(query)
            await self.db.commit()

            building = result.scalar_one_or_none()
            if building:
                logger.info(f"Restored building ID: {building_id}")
                return building

            logger.warning(f"Attempted to restore non-deleted building ID: {building_id}")
            raise BuildingNotFoundException(f"No deleted building found with ID {building_id}")

        except Exception as e:
            logger.error(f"Error restoring building {building_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(f"Failed to restore building: {str(e)}")