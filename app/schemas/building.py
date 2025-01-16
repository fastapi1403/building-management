from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel
from schemas.base import SchemaBase


class BuildingBase(SchemaBase):
    """
    Base Pydantic model for Building with common attributes
    """
    name: str
    total_floors: int
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities"
            }
        }

class BuildingCreate(BuildingBase):
    """
    Schema for creating a new building
    Inherits from BuildingBase and adds any create-specific fields
    """
    pass

class BuildingUpdate(SchemaBase):
    """
    Schema for updating an existing building
    All fields are optional
    """
    name: Optional[str] = None
    total_floors: Optional[int] = None
    description: Optional[str] = None

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Building Name",
                "total_floors": 10,
                "description": "Modern residential building with amenities"
            }
        }

class BuildingInDBBase(BuildingBase):
    """
    Base schema for Building in database
    Includes all common fields plus database-specific fields
    """
    id: int
    created_at: datetime = datetime.strptime("2025-01-16 15:55:47", "%Y-%m-%d %H:%M:%S")
    updated_at: datetime = datetime.strptime("2025-01-16 15:55:47", "%Y-%m-%d %H:%M:%S")
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities",
                "created_at": "2025-01-16 15:55:47",
                "updated_at": "2025-01-16 15:55:47",
                "is_deleted": False,
                "deleted_at": None,
            }
        }

class Building(BuildingInDBBase):
    """
    Schema for complete building information
    Used for responses that include all building data
    """
    pass

class BuildingInDB(BuildingInDBBase):
    """
    Schema for building information stored in database
    Used for internal processing
    """
    pass

class BuildingResponse(Building):
    """
    Schema for building response
    Inherits from Building and adds any response-specific fields
    """
    occupancy_rate: Optional[float] = None

    @property
    def calculate_occupancy_rate(self) -> float:
        """
        Calculate the occupancy rate as a percentage
        """
        if self.total_units and self.total_units > 0:
            return (self.occupied_units / self.total_units) * 100
        return 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities",
                # "created_at": "2025-01-16 15:55:47",
                # "updated_at": "2025-01-16 15:55:47",
                # "is_deleted": False,
                # "deleted_at": None,
            }
        }

class BuildingListResponse(SchemaBase):
    """
    Schema for list of buildings response
    """
    total: int
    items: list[BuildingResponse]

    class Config:
        json_schema_extra = {
            "example": {
                "total": 1,
                "items": [
                    {
                        "id": 1,
                        "name": "Sample Building",
                        "total_floors": 10,
                        "description": "Modern residential building with amenities",
                        # "created_at": "2025-01-16 15:55:47",
                        # "updated_at": "2025-01-16 15:55:47",
                        # "is_deleted": False,
                        # "deleted_at": None,
                    }
                ]
            }
        }