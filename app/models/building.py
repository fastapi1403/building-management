from typing import Optional, List

from sqlmodel import Field, Relationship

from app.models.base import TableBase


class Building(TableBase, table=True):
    """
    Building model inheriting from TableBase
    """
    __tablename__ = "buildings"
    __table_args__ = {'extend_existing': True}

    # Fields
    name: str = Field(
        ...,
        max_length=100,
        index=True,
        description="Name of the building"
    )
    total_floors: int = Field(
        ...,
        gt=0,
        description="Total number of floors in the building"
    )
    description: Optional[str] = Field(
        default=None,
        description="Description of the building"
    )

    # Relationships
    floors: List["Floor"] = Relationship(back_populates="building")
    funds: List["Fund"] = Relationship(back_populates="building")

    # Example configuration for OpenAPI schema
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Test Building",
                "total_floors": 10,
                "description": "A building with 10 floors located at 123 Test St"
            }
        }


# Import at the bottom to avoid circular imports
from app.models.floor import Floor  # noqa: E402
from app.models.fund import Fund  # noqa: E402
