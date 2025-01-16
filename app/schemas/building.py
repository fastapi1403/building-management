# app/schemas/building.py
from typing import Optional, List
from pydantic import Field, ConfigDict
from app.schemas.mixins import BaseSchema

class BuildingBase(BaseSchema):
    name: str = Field(..., description="Building name")
    total_floors: int = Field(..., description="Total number of floors")
    description: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **BaseSchema.model_config["json_schema_extra"]["example"],
                "name": "Sunrise Apartments",
                "total_floors": 7,
                "description": "Modern apartment building"
            }
        }
    )

class BuildingCreate(BuildingBase):
    """Schema for creating a building"""
    pass

class BuildingUpdate(BuildingBase):
    """Schema for updating a building"""
    name: Optional[str] = None
    total_floors: Optional[int] = None

class BuildingInDB(BuildingBase):
    """Schema for building in database"""
    id: int

class BuildingResponse(BuildingInDB):
    """Schema for building response"""
    pass