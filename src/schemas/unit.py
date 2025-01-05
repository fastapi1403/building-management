from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field
from .base import BaseSchema
from decimal import Decimal

class UnitBase(BaseSchema):
    number: str = Field(..., description="Unit number/identifier")
    floor: int = Field(..., ge=1, description="Floor number")
    area: Decimal = Field(..., gt=0, description="Unit area in square meters")
    bedrooms: int = Field(..., ge=0, description="Number of bedrooms")
    building_id: int = Field(..., description="ID of the associated building")
    is_occupied: bool = Field(default=False, description="Occupancy status")

class UnitCreate(UnitBase):
    pass

class UnitUpdate(BaseSchema):
    number: Optional[str] = None
    floor: Optional[int] = None
    area: Optional[Decimal] = None
    bedrooms: Optional[int] = None
    is_occupied: Optional[bool] = None

class UnitRead(UnitBase):
    id: int
    created_at: datetime
    updated_at: datetime

class UnitInDB(UnitRead):
    pass
