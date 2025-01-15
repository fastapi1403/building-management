from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_db
from app.crud import reports as crud
from typing import Optional
from datetime import date

router = APIRouter()

@router.get("/reports/income-expenses")
async def get_income_expenses_report(
    start_date: date,
    end_date: date,
    db: Session = Depends(get_db)
):
    """Generate income and expenses report"""
    return await crud.generate_income_expenses_report(
        db, start_date, end_date
    )


@router.get("/reports/occupancy")
async def get_occupancy_report(
    db: Session = Depends(get_db)
):
    """Generate occupancy report"""
    return await crud.generate_occupancy_report(db)


@router.get("/reports/debtors")
async def get_debtors_report(
    db: Session = Depends(get_db)
):
    """Generate debtors report"""
    return await crud.generate_debtors_report(db)


@router.get("/reports/utility-usage")
async def get_utility_usage_report(
    start_date: date,
    end_date: date,
    utility_type: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Generate utility usage report"""
    return await crud.generate_utility_usage_report(
        db, start_date, end_date, utility_type
    )