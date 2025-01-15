from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func
from datetime import datetime, UTC
import logging

from app.models.floor import Floor
from app.schemas.floor import FloorCreate, FloorUpdate
from core.exceptions import (
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    BusinessLogicException,
    DatabaseOperationException,
    handle_exceptions
)

# Configure logger
logger = logging.getLogger(__name__)


class FloorCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, floor_data: FloorCreate) -> Floor:
        """
        Create a new floor in the building
        """
        logger.info(f"Creating new floor with data: {floor_data}")

        # Check if floor number already exists in the building
        existing_floor = await self.get_by_floor_number(
            building_id=floor_data.building_id,
            floor_number=floor_data.floor_number
        )

        if existing_floor:
            logger.error(f"Floor {floor_data.floor_number} already exists in building {floor_data.building_id}")
            raise ResourceAlreadyExistsException(
                resource_type="Floor",
                identifier="floor_number",
                value=floor_data.floor_number,
                metadata={
                    "building_id": floor_data.building_id,
                    "attempted_at": datetime.now(UTC)
                }
            )

        floor = Floor(
            **floor_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(floor)
            await self.db.commit()
            await self.db.refresh(floor)
            logger.info(f"Successfully created floor with ID: {floor.id}")
            return floor
        except Exception as e:
            logger.error(f"Error creating floor: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail="Failed to create floor",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def get(self, floor_id: int) -> Optional[Floor]:
        """
        Get floor by ID
        """
        logger.info(f"Fetching floor with ID: {floor_id}")

        query = select(Floor).where(
            and_(
                Floor.id == floor_id,
                Floor.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(query)
        floor = result.scalar_one_or_none()

        if not floor:
            logger.warning(f"Floor with ID {floor_id} not found")
            raise ResourceNotFoundException(
                resource_type="Floor",
                resource_id=floor_id
            )

        return floor

    @handle_exceptions
    async def get_by_floor_number(
            self,
            building_id: int,
            floor_number: int
    ) -> Optional[Floor]:
        """
        Get floor by floor number in a specific building
        """
        logger.info(f"Fetching floor number {floor_number} in building {building_id}")

        query = select(Floor).where(
            and_(
                Floor.building_id == building_id,
                Floor.floor_number == floor_number,
                Floor.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    @handle_exceptions
    async def get_multi(
            self,
            building_id: Optional[int] = None,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Floor]:
        """
        Get multiple floors with optional filtering
        """
        logger.info(f"Fetching floors with filters: {filters}")

        query = select(Floor).where(Floor.deleted_at.is_(None))

        if building_id:
            query = query.where(Floor.building_id == building_id)

        if filters:
            if 'min_units' in filters:
                query = query.where(Floor.total_units >= filters['min_units'])
            if 'max_units' in filters:
                query = query.where(Floor.total_units <= filters['max_units'])

        query = query.offset(skip).limit(limit)
        result = await self.db.execute(query)

        return result.scalars().all()

    @handle_exceptions
    async def update(
            self,
            floor_id: int,
            floor_data: FloorUpdate
    ) -> Floor:
        """
        Update floor details
        """
        logger.info(f"Updating floor {floor_id} with data: {floor_data}")

        floor = await self.get(floor_id)

        update_data = floor_data.dict(exclude_unset=True)

        if 'total_units' in update_data:
            # Validate if new total units is less than current occupied units
            occupied_units = await self.get_occupied_units_count(floor_id)
            if update_data['total_units'] < occupied_units:
                raise BusinessLogicException(
                    detail=f"Cannot reduce total units below current occupied units ({occupied_units})",
                    metadata={
                        "current_occupied": occupied_units,
                        "requested_total": update_data['total_units']
                    }
                )

        for field, value in update_data.items():
            setattr(floor, field, value)

        floor.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(floor)
            logger.info(f"Successfully updated floor {floor_id}")
            return floor
        except Exception as e:
            logger.error(f"Error updating floor {floor_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail="Failed to update floor",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def delete(self, floor_id: int) -> bool:
        """
        Soft delete a floor
        """
        logger.info(f"Attempting to delete floor {floor_id}")

        floor = await self.get(floor_id)

        # Check if floor has any occupied units
        occupied_units = await self.get_occupied_units_count(floor_id)
        if occupied_units > 0:
            raise BusinessLogicException(
                detail="Cannot delete floor with occupied units",
                metadata={"occupied_units": occupied_units}
            )

        floor.deleted_at = datetime.now(UTC)

        try:
            await self.db.commit()
            logger.info(f"Successfully deleted floor {floor_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting floor {floor_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="delete",
                detail="Failed to delete floor",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def get_occupied_units_count(self, floor_id: int) -> int:
        """
        Get count of occupied units in a floor
        """
        from app.models.unit import Unit  # Import here to avoid circular imports

        query = select(func.count(Unit.id)).where(
            and_(
                Unit.floor_id == floor_id,
                Unit.is_occupied.is_(True),
                Unit.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(query)
        return result.scalar_one()

    @handle_exceptions
    async def get_floor_statistics(self, floor_id: int) -> Dict[str, Any]:
        """
        Get floor statistics including occupancy rate, maintenance status, etc.
        """
        floor = await self.get(floor_id)

        from app.models.unit import Unit

        # Get total and occupied units
        total_query = select(func.count(Unit.id)).where(
            and_(
                Unit.floor_id == floor_id,
                Unit.deleted_at.is_(None)
            )
        )
        occupied_query = select(func.count(Unit.id)).where(
            and_(
                Unit.floor_id == floor_id,
                Unit.is_occupied.is_(True),
                Unit.deleted_at.is_(None)
            )
        )

        total_units = await self.db.execute(total_query)
        occupied_units = await self.db.execute(occupied_query)

        total = total_units.scalar_one()
        occupied = occupied_units.scalar_one()

        return {
            "floor_number": floor.floor_number,
            "total_units": total,
            "occupied_units": occupied,
            "vacancy_rate": ((total - occupied) / total * 100) if total > 0 else 0,
            "occupancy_rate": (occupied / total * 100) if total > 0 else 0,
            "last_updated": floor.updated_at
        }