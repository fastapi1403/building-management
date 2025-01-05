from typing import List, Optional
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.crud_building import crud_building
from src.schemas.building import BuildingCreate, BuildingUpdate

class BuildingService:
    @staticmethod
    async def get_building_details(db: AsyncSession, building_id: int):
        building = await crud_building.get_with_units(db, id=building_id)
        if not building:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Building not found"
            )
        return building
