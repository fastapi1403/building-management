from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.models.building import Building
from src.schemas.building import BuildingCreate, BuildingUpdate
from .base import CRUDBase

class CRUDBuilding(CRUDBase[Building, BuildingCreate, BuildingUpdate]):
    async def get_by_name(self, db: AsyncSession, *, name: str) -> Optional[Building]:
        query = select(self.model).where(self.model.name == name)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_with_units(self, db: AsyncSession, *, id: int) -> Optional[Building]:
        building = await self.get(db=db, id=id)
        if building:
            await db.refresh(building, ["units"])
        return building

crud_building = CRUDBuilding(Building)
