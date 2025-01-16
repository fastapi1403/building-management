from typing import Optional, List
from pydantic import Field, ConfigDict
from app.schemas.mixins import BaseSchema


class FloorBase(BaseSchema):
    """Base Floor Schema with common attributes"""
    number: int = Field(
        ...,
        description="Floor number",
        ge=-10,  # Allow basement floors
        le=200  # Reasonable max floor number
    )
    name: Optional[str] = Field(
        default=None,
        description="Floor name or designation",
        max_length=100
    )
    building_id: int = Field(
        ...,
        description="ID of the building this floor belongs to"
    )
    total_units: Optional[int] = Field(
        default=None,
        description="Maximum number of units on this floor",
        gt=0
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the floor"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **BaseSchema.model_config["json_schema_extra"]["example"],
                "number": 1,
                "name": "First Floor",
                "building_id": 1,
                "total_units": 8,
                "description": "Main residential floor",
            }
        }
    )


class FloorCreate(FloorBase):
    """Schema for creating a new floor"""
    pass


class FloorUpdate(BaseSchema):
    """Schema for updating an existing floor"""
    name: Optional[str] = Field(
        default=None,
        max_length=100
    )
    total_units: Optional[int] = Field(default=None, gt=0)
    description: Optional[str] = None


class FloorInDB(FloorBase):
    """Schema for floor as stored in database"""
    id: int = Field(..., description="Unique identifier for the floor")


class FloorResponse(FloorInDB):
    """Schema for floor response"""
    total_units: Optional[int] = Field(
        default=0,
        description="Current number of units on the floor"
    )
    occupied_units: Optional[int] = Field(
        default=0,
        description="Number of occupied units on the floor"
    )
    vacant_units: Optional[int] = Field(
        default=0,
        description="Number of vacant units on the floor"
    )


class FloorBulkCreate(BaseSchema):
    """Schema for bulk floor creation"""
    floors: List[FloorCreate] = Field(
        description="List of floors to create",
        min_length=1
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **BaseSchema.model_config["json_schema_extra"]["example"],
                "floors": [
                    {
                        "number": 1,
                        "name": "First Floor",
                        "building_id": 1,
                        "area": 500.75,
                        "total_units": 8,
                        "description": "Main residential floor",
                    }
                ]
            }
        }
    )


class FloorFilter(BaseSchema):
    """Schema for filtering floors"""
    building_id: Optional[int] = None


class FloorStatistics(BaseSchema):
    """Schema for floor statistics"""
    total_floors: int = Field(..., description="Total number of floors")
    total_units: int = Field(..., description="Total number of units")
    occupied_units: int = Field(..., description="Total number of occupied units")
    vacant_units: int = Field(..., description="Total number of vacant units")

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                **BaseSchema.model_config["json_schema_extra"]["example"],
                "total_floors": 10,
                "total_units": 80,
                "occupied_units": 65,
                "vacant_units": 15,
            }
        }
    )