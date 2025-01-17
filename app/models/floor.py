from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base import TableBase


class Floor(TableBase, table=True):
    """
    Model for representing a floor in a building
    """
    __tablename__ = "floors"
    # __table_args__ = {'extend_existing': True}

    building_id: int = Field(foreign_key="buildings.id", description="ID of the building this floor belongs to")
    number: int = Field(description="Floor number")
    name: str = Field(description="Name of the floor")
    total_units: int = Field(description="Total number of units on the floor")
    description: Optional[str] = Field(default=None, description="Description of the floor")

    # Relationships
    building: "Building" = Relationship(back_populates="floors")
    units: List["Unit"] = Relationship(back_populates="floor")
    costs: List["Cost"] = Relationship(back_populates="floor")

    class Config:
        json_schema_extra = {
            "example": {
                "building_id": 1,
                "number": 2,
                "name": "Second Floor",
                "total_units": 10,
                "description": "Second floor with 10 units"
            }
        }


# Move these imports to the bottom to avoid circular imports
from app.models.building import Building  # noqa: E402
from app.models.unit import Unit  # noqa: E402
from app.models.cost import Cost  # noqa: E402
