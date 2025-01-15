from typing import Optional
from pydantic import BaseModel, Field, EmailStr
from .base import TimeStampSchema


class UnitBase(BaseModel):
    floor_id: int = Field(..., description="ID of the floor")
    unit_number: str = Field(..., description="Unit number")
    area: float = Field(..., gt=0, description="Area in square meters")
    has_parking: bool = Field(default=False, description="Whether unit has parking")
    parking_space_number: Optional[str] = Field(None, description="Parking space number")
    is_occupied: bool = Field(default=False, description="Whether unit is occupied")
    resident_count: int = Field(default=0, description="Number of residents")
    constant_extra_charge: float = Field(default=0.0, description="Constant extra charge")


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    floor_id: Optional[int] = None
    unit_number: Optional[str] = None
    area: Optional[float] = None


class Unit(UnitBase, TimeStampSchema):
    id: int


class UnitDetail(Unit):
    owner_name: Optional[str]
    tenant_name: Optional[str]
    total_charges: float
    unpaid_charges: float

# ------------------------------------------

from typing import Optional
from pydantic import Field, condecimal
from . import BaseSchema, TimeStampSchema


class UnitBase(BaseSchema):
    floor_id: int = Field(..., description="ID of the floor")
    unit_number: str = Field(..., description="Unit number")
    area: condecimal(max_digits=10, decimal_places=2) = Field(..., description="Unit area in square meters")
    has_parking: bool = Field(default=False, description="Whether unit has parking")
    parking_space_number: Optional[str] = Field(None, description="Parking space number if available")
    is_occupied: bool = Field(default=False, description="Whether unit is currently occupied")
    resident_count: int = Field(default=0, description="Number of residents")
    constant_extra_charge: condecimal(max_digits=10, decimal_places=2) = Field(
        default=0.0,
        description="Constant extra charge for this unit"
    )


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    floor_id: Optional[int] = None
    unit_number: Optional[str] = None
    area: Optional[condecimal(max_digits=10, decimal_places=2)] = None


class Unit(UnitBase, TimeStampSchema):
    id: int

# ------------------------------------------

rom typing import Optional
from .base import TimeStampSchema


class UnitBase(BaseModel):
    floor_id: int
    unit_number: str
    area: float
    has_parking: bool = False
    parking_space_number: Optional[str] = None
    is_occupied: bool = False
    resident_count: int = 0
    constant_extra_charge: float = 0.0


class UnitCreate(UnitBase):
    pass


class UnitUpdate(UnitBase):
    floor_id: Optional[int] = None
    unit_number: Optional[str] = None
    area: Optional[float] = None


class Unit(UnitBase, TimeStampSchema):
    id: int
    owner_id: Optional[int] = None
    tenant_id: Optional[int] = None
