from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, constr, condecimal
from decimal import Decimal
from enum import Enum

from models.charge import ChargeType, ChargeStatus, ChargeFrequency


# Base Schema
class ChargeBase(BaseModel):
    title: constr(min_length=3, max_length=100)
    description: constr(max_length=500)
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)
    type: ChargeType
    status: Optional[ChargeStatus] = ChargeStatus.PENDING
    due_date: date
    frequency: ChargeFrequency = ChargeFrequency.ONCE
    recurring: bool = False

    # Related entities
    building_id: int
    unit_id: Optional[int] = None
    owner_id: Optional[int] = None
    tenant_id: Optional[int] = None

    # Additional fields
    is_taxable: bool = False
    tax_rate: condecimal(ge=0, le=100, decimal_places=2) = Decimal("0.00")
    notes: Optional[str] = None

    @validator('due_date')
    def validate_due_date(cls, v):
        if v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v


# Create Schema
class ChargeCreate(ChargeBase):
    generated_by: constr(max_length=100) = Field(default="fastapi1403")


# Update Schema
class ChargeUpdate(BaseModel):
    title: Optional[constr(min_length=3, max_length=100)]
    description: Optional[constr(max_length=500)]
    amount: Optional[condecimal(gt=0, max_digits=10, decimal_places=2)]
    status: Optional[ChargeStatus]
    due_date: Optional[date]
    notes: Optional[str]
    is_taxable: Optional[bool]
    tax_rate: Optional[condecimal(ge=0, le=100, decimal_places=2)]

    @validator('due_date')
    def validate_due_date(cls, v):
        if v and v < date.today():
            raise ValueError("Due date cannot be in the past")
        return v


# DB Schema
class ChargeInDB(ChargeBase):
    id: int
    amount_paid: condecimal(ge=0, max_digits=10, decimal_places=2) = Decimal("0.00")
    last_payment_date: Optional[datetime]
    payment_reference: Optional[str]
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Response Schemas
class ChargeResponse(ChargeInDB):
    total_amount: condecimal(max_digits=10, decimal_places=2)
    balance_due: condecimal(max_digits=10, decimal_places=2)
    is_overdue: bool
    days_overdue: Optional[int]

    @validator('total_amount', pre=True)
    def calculate_total_amount(cls, v, values):
        amount = values.get('amount', Decimal("0.00"))
        tax_rate = values.get('tax_rate', Decimal("0.00"))
        if values.get('is_taxable', False):
            return amount + (amount * tax_rate / 100)
        return amount

    @validator('balance_due', pre=True)
    def calculate_balance_due(cls, v, values):
        total = values.get('total_amount', Decimal("0.00"))
        paid = values.get('amount_paid', Decimal("0.00"))
        return max(Decimal("0.00"), total - paid)

    @validator('is_overdue', pre=True)
    def calculate_is_overdue(cls, v, values):
        due_date = values.get('due_date')
        status = values.get('status')
        if not due_date or status == ChargeStatus.PAID:
            return False
        return due_date < date.today()

    @validator('days_overdue', pre=True)
    def calculate_days_overdue(cls, v, values):
        if not values.get('is_overdue'):
            return None
        due_date = values.get('due_date')
        return (date.today() - due_date).days


class ChargeList(BaseModel):
    charges: List[ChargeResponse]
    total_count: int
    total_amount: condecimal(max_digits=12, decimal_places=2)
    total_paid: condecimal(max_digits=12, decimal_places=2)
    total_pending: condecimal(max_digits=12, decimal_places=2)


# Payment Schema
class ChargePayment(BaseModel):
    amount: condecimal(gt=0, max_digits=10, decimal_places=2)
    payment_method: str = Field(..., max_length=50)
    payment_reference: Optional[str] = Field(None, max_length=100)
    payment_date: datetime = Field(default_factory=lambda: datetime.now())
    notes: Optional[str]


# Filter Schema
class ChargeFilter(BaseModel):
    status: Optional[List[ChargeStatus]]
    type: Optional[List[ChargeType]]
    due_date_from: Optional[date]
    due_date_to: Optional[date]
    min_amount: Optional[condecimal(ge=0)]
    max_amount: Optional[condecimal(ge=0)]
    is_overdue: Optional[bool]
    unit_id: Optional[int]
    owner_id: Optional[int]
    tenant_id: Optional[int]


# Statistics Schema
class ChargeStatistics(BaseModel):
    total_charges: int
    total_amount: condecimal(max_digits=12, decimal_places=2)
    total_paid: condecimal(max_digits=12, decimal_places=2)
    total_pending: condecimal(max_digits=12, decimal_places=2)
    overdue_charges: int
    overdue_amount: condecimal(max_digits=12, decimal_places=2)
    collection_rate: float
    average_days_to_pay: Optional[float]
    by_type: Dict[ChargeType, condecimal]
    by_status: Dict[ChargeStatus, int]
    monthly_totals: List[Dict[str, Any]]

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }