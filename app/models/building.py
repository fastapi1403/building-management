from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from mixins import TimestampMixin, SoftDeleteMixin
from app.models.floor import Floor
from app.models.fund import Fund

class Building(SQLModel, SoftDeleteMixin, TimestampMixin, table=True):
    __tablename__ = "buildings"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(..., index=True)
    total_floors: int
    description: Optional[str] = None

    # Relationships
    floors: List["Floor"] = Relationship(back_populates="building")
    funds: List["Fund"] = Relationship(back_populates="building")

Building.model_rebuild()