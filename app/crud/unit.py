from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.crud.base import CRUDBase
from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate
from app.utils.logger import log

class CRUDUnit(CRUDBase[Unit, UnitCreate, UnitUpdate]):
    async def get_by_floor(self, db: AsyncSession, *, floor_id: int) -> List[Unit]:
        try:
            query = select(self.model).where(self.model.floor_id == floor_id)
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            log.error(f"Error retrieving units for floor {floor_id}: {str(e)}")
            raise

    async def get_vacant_units(self, db: AsyncSession) -> List[Unit]:
        try:
            query = select(self.model).where(self.model.status == "vacant")
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            log.error(f"Error retrieving vacant units: {str(e)}")
            raise

crud_unit = CRUDUnit(Unit)