from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema
from decimal import Decimal

class TransactionBase(BaseSchema):
    amount: Decimal = Field(..., gt=0, description="Transaction amount")
    transaction_type: str = Field(..., description="Type of transaction (income/expense)")
    category: str = Field(..., description="Transaction category")
    description: str = Field(..., description="Transaction description")
    date: datetime = Field(default_factory=datetime.utcnow, description="Transaction date")

class TransactionCreate(TransactionBase):
    pass

class TransactionUpdate(BaseSchema):
    amount: Optional[Decimal] = None
    category: Optional[str] = None
    description: Optional[str] = None
    date: Optional[datetime] = None

class TransactionRead(TransactionBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TransactionInDB(TransactionRead):
    pass
