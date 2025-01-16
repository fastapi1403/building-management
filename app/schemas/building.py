from typing import Optional, List
from pydantic import Field, ConfigDict
from app.schemas.mixins import BaseSchema
from db import SchemaBase


class BuildingBase(SchemaBase):
    """Base Building Schema with common attributes"""
    name: str = Field(
        ...,
        description="Name of the building",
        min_length=2,
        max_length=100
    )
    total_floors: int = Field(
        ...,
        description="Total number of floors",
        gt=0
    )
    description: Optional[str] = Field(
        default=None,
        description="Additional details about the building"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "Sunset Towers",
                "total_floors": 10,
                "description": "Modern residential complex with amenities"
            }
        }
    )


class BuildingCreate(SchemaBase):
    """Schema for creating a new building"""
    pass


class BuildingUpdate(SchemaBase):
    """Schema for updating an existing building"""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    total_floors: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None


class BuildingResponse(SchemaBase):
    """Schema for building response with additional information"""
    id: int = Field(..., description="Unique identifier for the building")
    created_at: str
    updated_at: str
    occupied_units: int = Field(
        default=0,
        description="Number of currently occupied units"
    )
    vacant_units: int = Field(
        default=0,
        description="Number of vacant units"
    )