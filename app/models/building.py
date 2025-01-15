from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from base import TimestampModel


class Building(TimestampModel, table=True):
    __tablename__ = "buildings"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)
    address: str
    total_floors: int
    has_elevator: bool = Field(default=False)
    has_parking: bool = Field(default=False)
    total_parking_spaces: int = Field(default=0)
    has_boiler_room: bool = Field(default=False)
    description: Optional[str] = None

    # Relationships
    floors: List["Floor"] = Relationship(back_populates="building")
    funds: List["Fund"] = Relationship(back_populates="building")

    class Config:
        schema_extra = {
            "example": {
                "name": "Sunrise Apartments",
                "address": "123 Main Street",
                "total_floors": 5,
                "has_elevator": True,
                "has_parking": True,
                "total_parking_spaces": 10,
                "has_boiler_room": True
            }
        }
