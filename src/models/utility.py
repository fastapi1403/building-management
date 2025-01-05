from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Utility(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="building.id")
    utility_type: str  # water, electricity, gas
    reading_date: datetime
    reading_value: float
    cost_per_unit: float
    total_cost: float
    bill_number: Optional[str] = None
    payment_status: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    building: "Building" = Relationship(back_populates="utilities")
