from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.charge import Charge
from src.schemas.charge import ChargeCreate, ChargeUpdate
from .base import CRUDBase

class CRUDCharge(CRUDBase[Charge, ChargeCreate, ChargeUpdate]):
    async def get_unit_charges(
        self,
        db: AsyncSession,
        *,
        unit_id: int,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None,
        is_paid: Optional[bool] = None
    ) -> List[Charge]:
        filters = [Charge.unit_id == unit_id]
        if start_date and end_date:
            filters.append(Charge.date.between(start_date, end_date))
        if is_paid is not None:
            filters.append(Charge.is_paid == is_paid)
        query = select(Charge).where(and_(*filters))
        result = await db.execute(query)
        return result.scalars().all()

crud_charge = CRUDCharge(Charge)
