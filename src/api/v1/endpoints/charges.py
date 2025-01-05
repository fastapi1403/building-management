from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from datetime import date
from src.db.session import get_db
from src.crud import crud_charge
from src.schemas.charge import ChargeCreate, ChargeUpdate, ChargeRead
from src.services.charge_calculator import ChargeCalculator

router = APIRouter()
calculator = ChargeCalculator()

@router.post("/calculate-monthly", response_model=List[ChargeRead])
async def calculate_monthly_charges(
    *,
    db: AsyncSession = Depends(get_db),
    month: int,
    year: int
):
    Calculate monthly charges for all units.
    charges = await calculator.calculate_monthly_charges(db, month, year)
    return charges
