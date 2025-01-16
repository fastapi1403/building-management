from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from db import TableBase


class Building(TableBase):
    """
       Building model inheriting from TableBase
    """

    name: str = Field(
        ...,
        max_length=100,
        index=True
    )
    total_floors: int = Field(
        ...,
        gt=0
    )
    description: Optional[str] = None

    # Relationships
    floors: List["Floor"] = Relationship(back_populates="building")
    funds: List["Fund"] = Relationship(back_populates="building")

    class Config:
        schema_extra = {
            "example": {
                "name": "Test Building",
                "address": "123 Test St",
                "total_floors": 10,
                "year_built": 2023
            }
        }

from app.models.floor import Floor
from app.models.fund import Fund
