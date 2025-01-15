from typing import Optional, List
from pydantic import BaseModel, Field
from .base import TimeStampSchema


class FundBase(BaseModel):
    building_id: int = Field(..., description="ID of the building")
    name: str = Field(..., description="Name of the fund")
    balance: float = Field(default=0.0, description="Current balance")


class FundCreate(FundBase):
    pass


class FundUpdate(FundBase):
    name: Optional[str] = None
    balance: Optional[float] = None


class Fund(FundBase, TimeStampSchema):
    id: int


class FundDetail(Fund):
    total_income: float
    total_expenses: float
    recent_transactions: List["TransactionBase"]


# --------------------------

from typing import Optional
from pydantic import Field, condecimal
from . import BaseSchema, TimeStampSchema


class FundBase(BaseSchema):
    building_id: int = Field(..., description="ID of the building")
    name: str = Field(..., description="Name of the fund")
    balance: condecimal(max_digits=10, decimal_places=2) = Field(
        default=0.0,
        description="Current balance of the fund"
    )


class FundCreate(FundBase):
    pass


class FundUpdate(FundBase):
    building_id: Optional[int] = None
    name: Optional[str] = None
    balance: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class Fund(FundBase, TimeStampSchema):
    id: int