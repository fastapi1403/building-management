from typing import Optional, Dict
from datetime import date
from pydantic import BaseModel, Field
from .base import TimeStampSchema
from ..models.cost import CostType, DivisionMethod


class CostBase(BaseModel):
    type: CostType
    amount: float = Field(..., gt=0, description="Cost amount")
    date: date
    description: str = Field(..., description="Cost description")
    division_method: DivisionMethod
    is_warm_month: bool = Field(default=True, description="Whether this is a warm month")
    assigned_to_owner: bool = Field(default=False, description="Whether cost is assigned to owner")
    custom_division_rules: Optional[Dict] = Field(None, description="Custom division rules")


class CostCreate(CostBase):
    pass


class CostUpdate(CostBase):
    amount: Optional[float] = None
    description: Optional[str] = None
    division_method: Optional[DivisionMethod] = None
    is_warm_month: Optional[bool] = None
    assigned_to_owner: Optional[bool] = None
    custom_division_rules: Optional[Dict] = None


class Cost(CostBase, TimeStampSchema):
    id: int


class CostDetail(Cost):
    distributed_amount: float
    affected_units: int

# --------------------------------------------

from typing import Optional, Dict
from datetime import date
from pydantic import Field, condecimal
from . import BaseSchema, TimeStampSchema
from app.models.cost import CostType, DivisionMethod


class CostBase(BaseSchema):
    type: CostType = Field(..., description="Type of cost")
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Cost amount")
    date: date = Field(..., description="Date of the cost")
    description: str = Field(..., description="Cost description")
    division_method: DivisionMethod = Field(..., description="Method of cost division")
    is_warm_month: bool = Field(default=True, description="Whether this is a warm month")
    assigned_to_owner: bool = Field(default=False, description="Whether cost is assigned to owner")
    custom_division_rules: Optional[Dict] = Field(None, description="Custom rules for division")


class CostCreate(CostBase):
    pass


class CostUpdate(CostBase):
    type: Optional[CostType] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    date: Optional[date] = None
    description: Optional[str] = None
    division_method: Optional[DivisionMethod] = None


class Cost(CostBase, TimeStampSchema):
    id: int