from enum import Enum
from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base import TableBase


# Enumeration for unit types
class UnitType(str, Enum):
    RESIDENTIAL = "residential"
    COMMERCIAL = "commercial"
    OFFICE = "office"
    RETAIL = "retail"
    PARKING = "parking"


# Enumeration for unit statuses
class UnitStatus(str, Enum):
    VACANT = "vacant"
    OCCUPIED = "occupied"
    MAINTENANCE = "maintenance"
    RESERVED = "reserved"


# Model for representing a unit in the building management system
class Unit(TableBase, table=True):
    __tablename__ = "units"
    # __table_args__ = {'extend_existing': True}

    floor_id: int = Field(foreign_key="floors.id", description="ID of the associated floor")
    unit_number: str = Field(..., index=True, description="Unique number of the unit")
    owner_id: int = Field(foreign_key="owners.id", description="ID of the owner of this unit")
    type: UnitType = Field(default=UnitType.RESIDENTIAL, description="Type of the unit")
    status: UnitStatus = Field(default=UnitStatus.OCCUPIED, description="Status of the unit")
    area: float = Field(description="Area of the unit in square meters")
    has_parking: bool = Field(default=False, description="Whether the unit has an associated parking space")
    parking_space_number: Optional[str] = Field(default=None, description="Parking space number if available")
    # is_occupied: bool = Field(default=False, description="Whether the unit is currently vacant") # must calculate from tenant
    # resident_count: int = Field(default=0, description="Number of residents in the unit") # must calculate from tenant
    constant_extra_charge: float = Field(default=0.0, description="Any constant extra charge associated with the unit")
    notes: Optional[str] = Field(default=None, description="Additional notes about the unit")

    # Relationships
    floor: "Floor" = Relationship(back_populates="units")
    owner: Optional["Owner"] = Relationship(back_populates="units")
    tenant: Optional["Tenant"] = Relationship(back_populates="unit")
    charges: List["Charge"] = Relationship(back_populates="unit")
    costs: List["Cost"] = Relationship(back_populates="unit")

    class Config:
        json_schema_extra = {
            "example": {
                "floor_id": 1,
                "unit_number": "101A",
                "type": "residential",
                "status": "occupied",
                "area": 75.0,
                "has_parking": True,
                "parking_space_number": "P1",
                "is_occupied": True,
                "resident_count": 4,
                "constant_extra_charge": 100.0
            }
        }


# Import at the bottom to avoid circular imports
from app.models.charge import Charge  # noqa: E402
from app.models.owner import Owner  # noqa: E402
from app.models.floor import Floor  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402
from app.models.cost import Cost  # noqa: E402
