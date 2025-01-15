from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from . import TimeStampModel


class Tenant(TimeStampModel, table=True):
    __tablename__ = "tenants"

    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="units.id")
    name: str = Field(..., index=True)
    phone: str
    email: Optional[str] = None
    national_id: str = Field(..., unique=True)
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    occupant_count: int = Field(default=1)

    # Relationships
    unit: "Unit" = Relationship(back_populates="tenant")
    charges: List["Charge"] = Relationship(back_populates="tenant")
