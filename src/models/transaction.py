from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from src.core.constants import TransactionType

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    amount: float
    transaction_type: TransactionType
    description: str
    date: datetime = Field(default_factory=datetime.utcnow)
    reference_number: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
