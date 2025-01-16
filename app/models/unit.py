from enum import Enum
from typing import Optional, List

from sqlmodel import Field, Relationship

from app.db import TableBase


# from mixins import TimestampMixin, SoftDeleteMixin
# from app.models.owner import Owner
# from app.models.tenant import Tenant
# from app.models.charge import Charge
# from app.models.floor import Floor


class UnitType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    OFFICE = "office"
    RETAIL = "retail"
    PARKING = "parking"


class UnitStatus(str, Enum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    RESERVED = "reserved"


class Unit(TableBase, table=True):
    __tablename__ = "units"

    floor_id: int = Field(foreign_key="floors.id")
    unit_number: str = Field(..., index=True)
    type: UnitType = Field(default=UnitType.RESIDENTIAL)
    status: UnitStatus = Field(default=UnitStatus.OCCUPIED)
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


# Forward references for type hints
# from app.models.floor import Floor
from app.models.charge import Charge
from app.models.owner import Owner
from app.models.tenant import Tenant
