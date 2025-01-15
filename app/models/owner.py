from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from mixins import TimestampMixin, SoftDeleteMixin
from app.models.unit import Unit
from app.models.charge import Charge

class Owner(SQLModel, SoftDeleteMixin, TimestampMixin, table=True):
    __tablename__ = "owners"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)
    phone: str
    email: Optional[str] = None
    national_id: str = Field(..., unique=True)
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None

    # Relationships
    units: List["Unit"] = Relationship(back_populates="owner")
    charges: List["Charge"] = Relationship(back_populates="owner")


Owner.model_rebuild()