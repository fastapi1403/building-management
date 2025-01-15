from typing import Optional
from enum import Enum
from datetime import date
from sqlmodel import SQLModel, Field, Relationship
from . import TimeStampModel


class ChargeType(str, Enum):
    FIXED = "fixed"
    MANAGEMENT = "management"
    GAS = "gas"
    WATER = "water"
    ELECTRICITY = "electricity"
    CLEANING = "cleaning"
    REPAIR = "repair"
    MISCELLANEOUS = "miscellaneous"


class ChargeStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"


class Charge(TimeStampModel, table=True):
    __tablename__ = "charges"

    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="units.id")
    owner_id: Optional[int] = Field(foreign_key="owners.id")
    tenant_id: Optional[int] = Field(foreign_key="tenants.id")
    type: ChargeType
    amount: float
    due_date: date
    status: ChargeStatus = Field(default=ChargeStatus.PENDING)
    description: Optional[str] = None
    payment_date: Optional[date] = None
    payment_method: Optional[str] = None

    # Relationships
    unit: "Unit" = Relationship(back_populates="charges")
    owner: Optional["Owner"] = Relationship(back_populates="charges")
    tenant: Optional["Tenant"] = Relationship(back_populates="charges")
