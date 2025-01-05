from typing import List, Optional, Dict
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.unit import Unit
from src.schemas.unit import UnitCreate, UnitUpdate
from src.core.constants import UnitStatus
from .base import CRUDBase

class CRUDUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):
    async def get_by_filters(
        self,
        db: AsyncSession,
        *,
        building_id: Optional[int] = None,
        status: Optional[UnitStatus] = None,
        floor: Optional[int] = None
    ) -> List[Unit]:
        filters = []
        if building_id:
            filters.append(Unit.building_id == building_id)
        if status:
            filters.append(Unit.status == status)
        if floor:
            filters.append(Unit.floor == floor)
        query = select(Unit)
        if filters:
            query = query.where(and_(*filters))
        result = await db.execute(query)
        return result.scalars().all()

crud_unit = CRUDUnit(Unit)
