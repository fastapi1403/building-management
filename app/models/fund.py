from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from . import TimeStampModel


class Fund(TimeStampModel, table=True):
    __tablename__ = "funds"

    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="buildings.id")
    name: str
    balance: float = Field(default=0.0)

    # Relationships
    building: "Building" = Relationship(back_populates="funds")
    transactions: List["Transaction"] = Relationship(back_populates="fund")
