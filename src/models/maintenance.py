from typing import Optional
from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship

class Maintenance(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    building_id: int = Field(foreign_key="building.id")
    title: str
    description: str
    maintenance_type: str  # repair, regular, emergency
    cost: float
    start_date: datetime
    end_date: Optional[datetime] = None
    status: str = Field(default="pending")  # pending, in_progress, completed
    contractor: Optional[str] = None
    contractor_phone: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
