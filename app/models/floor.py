from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
# from app.models.building import Building
from app.models.unit import Unit
from app.models.base import TableBase


class Floor(TableBase, table=True):
    __tablename__ = "floors"
    __table_args__ = {'extend_existing': True}

    building_id: int = Field(foreign_key="buildings.id")
    number: int
    name: str
    total_units: int
    description: Optional[str] = None


    # Relationships
    building: "Building" = Relationship(back_populates="floors")
    units: List["Unit"] = Relationship(back_populates="floor")

# Forward references for type hints
from app.models.building import Building
from app.models.unit import Unit