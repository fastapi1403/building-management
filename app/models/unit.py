from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from enum import Enum

from app.models.mixins import SoftDeleteMixin, TimestampMixin
# from mixins import TimestampMixin, SoftDeleteMixin
# from app.models.owner import Owner
# from app.models.tenant import Tenant
# from app.models.charge import Charge
# from app.models.floor import Floor


class UnitType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    OFFICE = "office"


class Unit(SQLModel, SoftDeleteMixin, TimestampMixin, table=True):
    __tablename__ = "units"

    id: Optional[int] = Field(default=None, primary_key=True)
    floor_id: int = Field(foreign_key="floors.id")
    unit_number: str = Field(..., index=True)
    type: UnitType = Field(default=UnitType.RESIDENTIAL)
    area: float
    has_parking: bool = Field(default=False)
    parking_space_number: Optional[str] = None
    is_occupied: bool = Field(default=False)
    resident_count: int = Field(default=0)
    constant_extra_charge: float = Field(default=0.0)

    # Relationships
    floor: "Floor" = Relationship(back_populates="units")
    owner: Optional["Owner"] = Relationship(back_populates="units")
    tenant: Optional["Tenant"] = Relationship(back_populates="unit")
    charges: List["Charge"] = Relationship(back_populates="unit")

Unit.model_rebuild()