from typing import Optional, List
from pydantic import BaseModel, Field
from .base import TimeStampSchema


class FloorBase(BaseModel):
    building_id: int = Field(..., description="ID of the building")
    floor_number: int = Field(..., description="Floor number")
    total_units: int = Field(..., ge=1, description="Total number of units on this floor")


class FloorCreate(FloorBase):
    pass


class FloorUpdate(FloorBase):
    building_id: Optional[int] = None
    floor_number: Optional[int] = None
    total_units: Optional[int] = None


class Floor(FloorBase, TimeStampSchema):
    id: int


class FloorDetail(Floor):
    occupied_units: int
    total_residents: int


# ---------------------------------------

from typing import Optional, List
from pydantic import Field
from . import BaseSchema, TimeStampSchema


class FloorBase(BaseSchema):
    building_id: int = Field(..., description="ID of the building")
    floor_number: int = Field(..., description="Floor number")
    total_units: int = Field(..., ge=1, description="Total number of units on this floor")


class FloorCreate(FloorBase):
    pass


class FloorUpdate(FloorBase):
    building_id: Optional[int] = None
    floor_number: Optional[int] = None
    total_units: Optional[int] = None


class Floor(FloorBase, TimeStampSchema):
    id: int

# ---------------------------------------

from typing import Optional, List
from .base import TimeStampSchema


class FloorBase(BaseModel):
    building_id: int
    floor_number: int
    total_units: int


class FloorCreate(FloorBase):
    pass


class FloorUpdate(FloorBase):
    building_id: Optional[int] = None
    floor_number: Optional[int] = None
    total_units: Optional[int] = None


class Floor(FloorBase, TimeStampSchema):
    id: int
    units: List["Unit"] = []