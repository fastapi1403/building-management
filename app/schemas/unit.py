from typing import Optional
from pydantic import BaseModel, Field, field_validator, model_validator, ConfigDict
from enum import Enum
from datetime import datetime, UTC
from app.schemas.mixins import BaseSchema  # Add this import which was missing
from models.unit import UnitType, UnitStatus


class UnitBase(BaseModel):
    unit_number: str = Field(
        ...,
        min_length=1,
        max_length=10,
        description="Unique identifier for the unit within the building"
    )
    floor_id: int = Field(
        ...,
        gt=0,
        description="ID of the floor where this unit is located"
    )
    type: UnitType = Field(
        default=UnitType.RESIDENTIAL,
        description="Type of the unit (residential, commercial, etc.)"
    )
    area_sqft: float = Field(
        ...,
        gt=0,
        le=10000,
        description="Area of the unit in square feet"
    )
    status: UnitStatus = Field(
        default=UnitStatus.VACANT,
        description="Current status of the unit"
    )
    monthly_maintenance: float = Field(
        default=0.0,
        ge=0,
        description="Monthly maintenance charges"
    )
    current_owner_id: Optional[int] = Field(
        default=None,
        description="ID of the current owner of the unit"
    )

    model_config = ConfigDict(
        from_attributes=True
    )

    @field_validator('unit_number')
    @classmethod
    def validate_unit_number(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("Unit number must contain at least one digit")
        return v.upper()

    @field_validator('area_sqft')
    @classmethod
    def validate_area(cls, v: float) -> float:
        return round(v, 2)

    @model_validator(mode='after')
    def validate_status_and_owner(self) -> 'UnitBase':
        if self.status == UnitStatus.OCCUPIED and self.current_owner_id is None:
            raise ValueError("Occupied units must have an owner")
        return self

class UnitCreate(UnitBase):
    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "unit_number": "1501A",
                "floor_id": 15,
                "type": "residential",
                "area_sqft": 1250.75,
                "status": "vacant",
                "monthly_maintenance": 2500.00,
                "current_owner_id": None
            },
            "examples": [
                {
                    "summary": "Residential Unit",
                    "description": "Example of a residential unit creation",
                    "value": {
                        "unit_number": "1501A",
                        "floor_id": 15,
                        "type": "residential",
                        "area_sqft": 1250.75,
                        "status": "vacant",
                        "monthly_maintenance": 2500.00,
                        "current_owner_id": None
                    }
                },
                {
                    "summary": "Commercial Unit",
                    "description": "Example of a commercial unit creation",
                    "value": {
                        "unit_number": "1502B",
                        "floor_id": 15,
                        "type": "commercial",
                        "area_sqft": 2500.00,
                        "status": "reserved",
                        "monthly_maintenance": 5000.00,
                        "current_owner_id": 101
                    }
                }
            ]
        }
    )

class UnitUpdate(BaseModel):
    unit_number: Optional[str] = Field(
        None,
        min_length=1,
        max_length=10
    )
    type: Optional[UnitType] = None
    area_sqft: Optional[float] = Field(None, gt=0, le=10000)
    status: Optional[UnitStatus] = None
    monthly_maintenance: Optional[float] = Field(None, ge=0)
    current_owner_id: Optional[int] = None

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "status": "occupied",
                "monthly_maintenance": 2700.00,
                "current_owner_id": 123
            },
            "examples": [
                {
                    "summary": "Update Status",
                    "description": "Example of updating unit status",
                    "value": {
                        "status": "occupied",
                        "current_owner_id": 123
                    }
                },
                {
                    "summary": "Update Maintenance",
                    "description": "Example of updating maintenance fee",
                    "value": {
                        "monthly_maintenance": 2700.00
                    }
                }
            ]
        }
    )

    @model_validator(mode='after')
    def validate_partial_update(self) -> 'UnitUpdate':
        if self.status == UnitStatus.OCCUPIED and self.current_owner_id is None:
            raise ValueError("Cannot set status to occupied without an owner")
        return self

class UnitResponse(UnitBase, TimestampSchema):
    id: int
    last_maintenance_date: Optional[datetime] = Field(
        default=None,
        description="Date of the last maintenance check"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 157,
                "unit_number": "1501A",
                "floor_id": 15,
                "type": "residential",
                "area_sqft": 1250.75,
                "status": "vacant",
                "monthly_maintenance": 2500.00,
                "current_owner_id": None,
                "created_at": "2025-01-15T08:52:00Z",
                "updated_at": "2025-01-15T08:52:00Z",
                "deleted_at": None,
                "last_maintenance_date": "2025-01-01T10:00:00Z"
            },
            "examples": [
                {
                    "summary": "Vacant Residential Unit",
                    "description": "Example of a vacant residential unit response",
                    "value": {
                        "id": 157,
                        "unit_number": "1501A",
                        "floor_id": 15,
                        "type": "residential",
                        "area_sqft": 1250.75,
                        "status": "vacant",
                        "monthly_maintenance": 2500.00,
                        "current_owner_id": None,
                        "created_at": "2025-01-15T08:52:00Z",
                        "updated_at": "2025-01-15T08:52:00Z",
                        "deleted_at": None,
                        "last_maintenance_date": "2025-01-01T10:00:00Z"
                    }
                },
                {
                    "summary": "Occupied Commercial Unit",
                    "description": "Example of an occupied commercial unit response",
                    "value": {
                        "id": 158,
                        "unit_number": "1502B",
                        "floor_id": 15,
                        "type": "commercial",
                        "area_sqft": 2500.00,
                        "status": "occupied",
                        "monthly_maintenance": 5000.00,
                        "current_owner_id": 101,
                        "created_at": "2025-01-15T08:52:00Z",
                        "updated_at": "2025-01-15T08:52:00Z",
                        "deleted_at": None,
                        "last_maintenance_date": "2025-01-10T14:30:00Z"
                    }
                }
            ]
        }
    )

class UnitDetailResponse(UnitResponse):
    floor_number: int = Field(..., description="Floor number where the unit is located")
    owner_name: Optional[str] = Field(None, description="Name of the current owner")
    tenant_name: Optional[str] = Field(None, description="Name of the current tenant")
    occupancy_rate: Optional[float] = Field(
        None,
        description="Percentage of time the unit has been occupied"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "id": 157,
                "unit_number": "1501A",
                "floor_id": 15,
                "floor_number": 15,
                "type": "residential",
                "area_sqft": 1250.75,
                "status": "occupied",
                "monthly_maintenance": 2500.00,
                "current_owner_id": 123,
                "owner_name": "John Doe",
                "tenant_name": "Jane Smith",
                "occupancy_rate": 85.5,
                "created_at": "2025-01-15T08:52:00Z",
                "updated_at": "2025-01-15T08:52:00Z",
                "deleted_at": None,
                "last_maintenance_date": "2025-01-01T10:00:00Z"
            },
            "examples": [
                {
                    "summary": "Detailed Residential Unit",
                    "description": "Example of a detailed residential unit response",
                    "value": {
                        "id": 157,
                        "unit_number": "1501A",
                        "floor_id": 15,
                        "floor_number": 15,
                        "type": "residential",
                        "area_sqft": 1250.75,
                        "status": "occupied",
                        "monthly_maintenance": 2500.00,
                        "current_owner_id": 123,
                        "owner_name": "John Doe",
                        "tenant_name": "Jane Smith",
                        "occupancy_rate": 85.5,
                        "created_at": "2025-01-15T08:52:00Z",
                        "updated_at": "2025-01-15T08:52:00Z",
                        "deleted_at": None,
                        "last_maintenance_date": "2025-01-01T10:00:00Z"
                    }
                },
                {
                    "summary": "Detailed Commercial Unit",
                    "description": "Example of a detailed commercial unit response",
                    "value": {
                        "id": 158,
                        "unit_number": "1502B",
                        "floor_id": 15,
                        "floor_number": 15,
                        "type": "commercial",
                        "area_sqft": 2500.00,
                        "status": "occupied",
                        "monthly_maintenance": 5000.00,
                        "current_owner_id": 101,
                        "owner_name": "ABC Corporation",
                        "tenant_name": "XYZ Ltd",
                        "occupancy_rate": 95.0,
                        "created_at": "2025-01-15T08:52:00Z",
                        "updated_at": "2025-01-15T08:52:00Z",
                        "deleted_at": None,
                        "last_maintenance_date": "2025-01-10T14:30:00Z"
                    }
                }
            ]
        }
    )