from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema
from decimal import Decimal

class ChargeBase(BaseSchema):
    unit_id: int = Field(..., description="ID of the associated unit")
    amount: Decimal = Field(..., gt=0, description="Charge amount")
    description: str = Field(..., description="Charge description")
    due_date: datetime = Field(..., description="Due date for the charge")
    is_paid: bool = Field(default=False, description="Payment status")
    charge_type: str = Field(..., description="Type of charge")

class ChargeCreate(ChargeBase):
    pass

class ChargeUpdate(BaseSchema):
    amount: Optional[Decimal] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    is_paid: Optional[bool] = None

class ChargeRead(ChargeBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ChargeInDB(ChargeRead):
    pass
