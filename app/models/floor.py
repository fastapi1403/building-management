from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from base import TimestampMixin


class Floor(TimestampMixin, table=True):
    __tablename__ = "floors"

    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="buildings.id")
    floor_number: int
    total_units: int

    # Relationships
    building: "Building" = Relationship(back_populates="floors")
    units: List["Unit"] = Relationship(back_populates="floor")
