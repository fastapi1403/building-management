from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .base import BaseSchema

class BuildingBase(BaseSchema):
    name: str = Field(..., description="Name of the building")
    address: str = Field(..., description="Physical address of the building")
    floors: int = Field(..., ge=1, description="Number of floors in the building")
    units_count: int = Field(..., ge=1, description="Total number of units in the building")
    description: Optional[str] = Field(None, description="Optional description of the building")

class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseSchema):
    name: Optional[str] = None
    address: Optional[str] = None
    floors: Optional[int] = None
    units_count: Optional[int] = None
    description: Optional[str] = None

class BuildingRead(BuildingBase):
    id: int
    created_at: datetime
    updated_at: datetime

class BuildingInDB(BuildingRead):
    pass
