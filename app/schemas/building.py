from typing import Optional, List
from pydantic import BaseModel, Field
from .base import TimeStampSchema


class BuildingBase(BaseModel):
    name: str = Field(..., description="Name of the building")
    address: str = Field(..., description="Physical address of the building")
    total_floors: int = Field(..., ge=1, description="Total number of floors")
    has_elevator: bool = Field(default=False, description="Whether building has elevator")
    has_parking: bool = Field(default=False, description="Whether building has parking")
    total_parking_spaces: int = Field(default=0, description="Total number of parking spaces")
    has_boiler_room: bool = Field(default=False, description="Whether building has boiler room")


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    name: Optional[str] = None
    address: Optional[str] = None
    total_floors: Optional[int] = None


class Building(BuildingBase, TimeStampSchema):
    id: int

    class Config:
        from_attributes = True


class BuildingDetail(Building):
    total_units: int
    occupied_units: int
    total_residents: int
    total_income: float
    total_expenses: float

# --------------------------------------------

from typing import Optional, List
from pydantic import Field, EmailStr
from . import BaseSchema, TimeStampSchema


class BuildingBase(BaseSchema):
    name: str = Field(..., description="Name of the building")
    address: str = Field(..., description="Physical address of the building")
    total_floors: int = Field(..., ge=1, description="Total number of floors")
    has_elevator: bool = Field(default=False, description="Whether building has elevator")
    has_parking: bool = Field(default=False, description="Whether building has parking")
    total_parking_spaces: int = Field(default=0, description="Total number of parking spaces")
    has_boiler_room: bool = Field(default=False, description="Whether building has boiler room")


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    name: Optional[str] = None
    address: Optional[str] = None
    total_floors: Optional[int] = None


class Building(BuildingBase, TimeStampSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sunrise Apartments",
                "address": "123 Main Street",
                "total_floors": 5,
                "has_elevator": True,
                "has_parking": True,
                "total_parking_spaces": 10,
                "has_boiler_room": True,
                "created_at": "2025-01-08T13:08:32",
                "updated_at": "2025-01-08T13:08:32"
            }
        }


# ---------------------------------
from typing import Optional, List
from pydantic import BaseModel
from .base import TimeStampSchema


class BuildingBase(BaseModel):
    name: str
    address: str
    total_floors: int
    has_elevator: bool = False
    has_parking: bool = False
    total_parking_spaces: int = 0
    has_boiler_room: bool = False


class BuildingCreate(BuildingBase):
    pass


class BuildingUpdate(BuildingBase):
    name: Optional[str] = None
    address: Optional[str] = None
    total_floors: Optional[int] = None


class Building(BuildingBase, TimeStampSchema):
    id: int
    floors: List["Floor"] = []


