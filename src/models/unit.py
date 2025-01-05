from typing import Optional, List
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from src.core.constants import UnitStatus

class Unit(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="building.id")
    unit_number: str = Field(index=True)
    floor: int
    size: float
    rooms: int
    orientation: str  # North, South, East, West
    has_parking: bool = Field(default=False)
    has_storage: bool = Field(default=False)
    status: UnitStatus = Field(default=UnitStatus.VACANT)
    occupants_count: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    building: "Building" = Relationship(back_populates="units")
    owner: Optional["Owner"] = Relationship(back_populates="units")
    tenant: Optional["Tenant"] = Relationship(back_populates="units")
    charges: List["Charge"] = Relationship(back_populates="unit")
