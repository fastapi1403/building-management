from typing import Optional, List

from pydantic import ConfigDict
from sqlmodel import Field, Relationship

from app.db import TableBase


class Building(TableBase, table=True):
    """
       Building model inheriting from TableBase
    """
    __tablename__ = "buildings"

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

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "name": "Test Building",
                "address": "123 Test St",
                "total_floors": 10,
                "year_built": 2023
            }
        }
    )


# from app.models.floor import Floor
# from app.models.fund import Fund
