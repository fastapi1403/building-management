from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from . import TimeStampModel


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


class Transaction(TimeStampModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    fund_id: int = Field(foreign_key="funds.id")
    type: TransactionType
    amount: float
    description: str
    reference_number: Optional[str] = None

    # Relationships
    fund: "Fund" = Relationship(back_populates="transactions")
