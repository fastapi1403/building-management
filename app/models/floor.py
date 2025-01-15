from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from mixins import TimestampMixin, SoftDeleteMixin
from app.models.building import Building
from app.models.unit import Unit

class Floor(SQLModel, SoftDeleteMixin, TimestampMixin, table=True):
    __tablename__ = "floors"

    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="buildings.id")
    number: int
    name: str
    total_units: int
    description: Optional[str] = None


    # Relationships
    building: "Building" = Relationship(back_populates="floors")
    units: List["Unit"] = Relationship(back_populates="floor")

Floor.model_rebuild()