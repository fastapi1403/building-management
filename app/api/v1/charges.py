from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from app.db.session import get_db
from app.crud import charge as crud
from app.schemas.charge import Charge, ChargeCreate, ChargeUpdate

router = APIRouter()

@router.get("/charges/", response_model=List[Charge])
async def read_charges(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    charges = await crud.get_charges(db, skip=skip, limit=limit)
    return charges


@router.post("/charges/", response_model=Charge)
async def create_charge(
    charge: ChargeCreate,
    db: Session = Depends(get_db)
):
    return await crud.create_charge(db, charge)


@router.get("/charges/{charge_id}", response_model=Charge)
async def read_charge(
    charge_id: int,
    db: Session = Depends(get_db)
):
    charge = await crud.get_charge(db, charge_id)
    if charge is None:
        raise HTTPException(status_code=404, detail="Charge not found")
    return charge


@router.put("/charges/{charge_id}", response_model=Charge)
async def update_charge(
    charge_id: int,
    charge: ChargeUpdate,
    db: Session = Depends(get_db)
):
    updated_charge = await crud.update_charge(
        db, charge_id, charge
    )
    if updated_charge is None:
        raise HTTPException(status_code=404, detail="Charge not found")
    return updated_charge


@router.post("/charges/calculate-monthly")
async def calculate_monthly_charges(
    db: Session = Depends(get_db)
):
    """Calculate monthly charges for all units"""
    return await crud.calculate_monthly_charges(db)


@router.post("/charges/{charge_id}/pay")
async def pay_charge(
    charge_id: int,
    db: Session = Depends(get_db)
):
    """Mark a charge as paid"""
    updated_charge = await crud.pay_charge(db, charge_id)
    if updated_charge is None:
        raise HTTPException(status_code=404, detail="Charge not found")
    return updated_charge