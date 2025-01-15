from typing import Optional
from datetime import date
from pydantic import BaseModel, Field
from .base import TimeStampSchema
from ..models.charge import ChargeType, ChargeStatus


class ChargeBase(BaseModel):
    unit_id: int = Field(..., description="ID of the unit")
    owner_id: Optional[int] = Field(None, description="ID of the owner")
    tenant_id: Optional[int] = Field(None, description="ID of the tenant")
    type: ChargeType
    amount: float = Field(..., gt=0, description="Charge amount")
    due_date: date
    status: ChargeStatus = Field(default=ChargeStatus.PENDING)
    description: Optional[str] = Field(None, description="Charge description")
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None


class ChargeCreate(ChargeBase):
    pass


class ChargeUpdate(ChargeBase):
    amount: Optional[float] = None
    status: Optional[ChargeStatus] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None


class Charge(ChargeBase, TimeStampSchema):
    id: int


class ChargeDetail(Charge):
    unit_number: str
    owner_name: Optional[str]
    tenant_name: Optional[str]


# ------------------------------------

from typing import Optional
from datetime import date
from pydantic import Field, condecimal
from . import BaseSchema, TimeStampSchema
from app.models.charge import ChargeType, ChargeStatus


class ChargeBase(BaseSchema):
    unit_id: int = Field(..., description="ID of the unit")
    owner_id: Optional[int] = Field(None, description="ID of the owner")
    tenant_id: Optional[int] = Field(None, description="ID of the tenant")
    type: ChargeType = Field(..., description="Type of charge")
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Charge amount")
    due_date: date = Field(..., description="Due date for the charge")
    status: ChargeStatus = Field(default=ChargeStatus.PENDING, description="Status of the charge")
    description: Optional[str] = Field(None, description="Charge description")
    payment_date: Optional[date] = Field(None, description="Date of payment")
    payment_method: Optional[str] = Field(None, description="Method of payment")


class ChargeCreate(ChargeBase):
    pass


class ChargeUpdate(ChargeBase):
    unit_id: Optional[int] = None
    type: Optional[ChargeType] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    due_date: Optional[date] = None
    status: Optional[ChargeStatus] = None


class Charge(ChargeBase, TimeStampSchema):
    id: int