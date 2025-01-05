from typing import List, Dict
from decimal import Decimal
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.crud_unit import crud_unit
from src.crud.crud_charge import crud_charge
from src.schemas.charge import ChargeCreate

class ChargeCalculator:
    async def calculate_monthly_charges(
        self,
        db: AsyncSession,
        month: int,
        year: int
    ) -
        units = await crud_unit.get_occupied(db)
        charges = []
        for unit in units:
            charge = await self._calculate_unit_charges(unit, month, year)
            charges.append(charge)
        return charges
