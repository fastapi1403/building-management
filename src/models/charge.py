from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from src.core.constants import ChargeType, PaymentStatus

class Charge(SQLModel, table=True):
    __tablename__ = "charges"

    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="unit.id")
    amount: float
    charge_type: ChargeType
    description: Optional[str] = None
    due_date: datetime
    payment_status: PaymentStatus = Field(default=PaymentStatus.UNPAID)
    paid_amount: float = Field(default=0.0)
    paid_date: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    unit: "Unit" = Relationship(back_populates="charges")
