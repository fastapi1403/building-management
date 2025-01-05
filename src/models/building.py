from typing import List, Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Building(SQLModel, table=True):
    __tablename__ = "buildings"

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(index=True)
    address: str
    floors: int
    total_units: int
    has_elevator: bool = Field(default=False)
    has_parking: bool = Field(default=False)
    has_storage: bool = Field(default=False)
    description: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    units: List["Unit"] = Relationship(back_populates="building")
    utilities: List["Utility"] = Relationship(back_populates="building")
