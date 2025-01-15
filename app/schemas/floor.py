from typing import Optional, List
from pydantic import BaseModel, Field
from .base import TimestampSchema


class FloorBase(BaseModel):
    floor_number: int = Field(..., ge=0)
    total_units: int = Field(..., gt=0)
    building_id: int = Field(...)

    class Config:
        json_schema_extra = {
            "example": {
                "floor_number": 5,
                "total_units": 4,
                "building_id": 1
            }
        }


class FloorCreate(FloorBase):
    pass


class FloorUpdate(BaseModel):
    total_units: Optional[int] = Field(None, gt=0)

    class Config:
        json_schema_extra = {
            "example": {
                "total_units": 5
            }
        }


class FloorResponse(FloorBase, TimestampSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "floor_number": 5,
                "total_units": 4,
                "building_id": 1,
                "created_at": "2025-01-15T08:42:00Z",
                "updated_at": "2025-01-15T08:42:00Z",
                "deleted_at": None
            }
        }
