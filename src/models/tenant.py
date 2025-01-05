from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Tenant(SQLModel, table=True):
    __tablename__ = "tenants"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    email: str = Field(unique=True, index=True)
    phone: str
    national_id: str = Field(unique=True)
    contract_start: datetime
    contract_end: datetime
    deposit_amount: float
    monthly_rent: float
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    units: List["Unit"] = Relationship(back_populates="tenant")
