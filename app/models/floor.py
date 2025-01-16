from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
# from app.models.building import Building
from app.models.unit import Unit
from app.models.mixins import SoftDeleteMixin, TimestampMixin
from db import TableBase


class Floor(TableBase):
    building_id: int = Field(foreign_key="buildings.id")
    number: int
    name: str
    total_units: int
    description: Optional[str] = None


    # Relationships
    building: "Building" = Relationship(back_populates="floors")
    units: List["Unit"] = Relationship(back_populates="floor")

# Floor.model_rebuild()