from typing import Optional
from datetime import datetime
from pydantic import BaseModel, Field
from .base import TimeStampSchema
from ..models.transaction import TransactionType


class TransactionBase(BaseModel):
    fund_id: int = Field(..., description="ID of the fund")
    type: TransactionType
    amount: float = Field(..., gt=0, description="Transaction amount")
    description: str = Field(..., description="Transaction description")
    reference_number: Optional[str] = Field(None, description="Reference number")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    amount: Optional[float] = None
    description: Optional[str] = None


class Transaction(TransactionBase, TimeStampSchema):
    id: int


# ----------------------------------------

from typing import Optional
from datetime import datetime
from pydantic import Field, condecimal
from . import BaseSchema, TimeStampSchema
from app.models.transaction import TransactionType


class TransactionBase(BaseSchema):
    fund_id: int = Field(..., description="ID of the fund")
    type: TransactionType = Field(..., description="Type of transaction")
    amount: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Transaction amount")
    description: str = Field(..., description="Transaction description")
    reference_number: Optional[str] = Field(None, description="Reference number")


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    fund_id: Optional[int] = None
    type: Optional[TransactionType] = None
    amount: Optional[condecimal(max_digits=10, decimal_places=2)] = None
    description: Optional[str] = None


class Transaction(TransactionBase, TimeStampSchema):
    id: int