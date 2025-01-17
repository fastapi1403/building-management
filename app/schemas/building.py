from typing import Optional, List
from sqlmodel import Field
from app.schemas.base import SchemaBase

# Base Pydantic model for Building with common attributes
class BuildingBase(SchemaBase):
    name: str = Field(..., description="Name of the building")
    total_floors: int = Field(..., description="Total number of floors in the building")
    description: Optional[str] = Field(None, description="Description of the building")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities"
            }
        }

# Schema for creating a new building
class BuildingCreate(BuildingBase):
    pass

# Schema for updating an existing building
class BuildingUpdate(SchemaBase):
    name: Optional[str] = Field(None, description="Name of the building")
    total_floors: Optional[int] = Field(None, description="Total number of floors in the building")
    description: Optional[str] = Field(None, description="Description of the building")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Updated Building Name",
                "total_floors": 10,
                "description": "Modern residential building with amenities"
            }
        }

# Base schema for Building in database
class BuildingInDBBase(SchemaBase):

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities",
                "created_at": "2025-01-16T15:55:47",
                "updated_at": "2025-01-17T15:55:47",
                "is_deleted": False,
                "deleted_at": None,
            }
        }

# Schema for complete building information
class Building(BuildingInDBBase):
    pass

# Schema for building information stored in database
class BuildingInDB(BuildingInDBBase):
    pass

# Schema for building response
class BuildingResponse(Building):
    occupancy_rate: Optional[float] = Field(None, description="Occupancy rate of the building")

    @property
    def calculate_occupancy_rate(self) -> float:
        """
        Calculate the occupancy rate as a percentage
        """
        if hasattr(self, 'total_units') and self.total_units > 0:
            return (self.occupied_units / self.total_units) * 100
        return 0.0

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Sample Building",
                "total_floors": 10,
                "description": "Modern residential building with amenities",
                "occupancy_rate": 95.0,
            }
        }

# Schema for list of buildings response
class BuildingListResponse(SchemaBase):
    total: int = Field(..., description="Total number of buildings")
    items: List[BuildingResponse] = Field(..., description="List of building responses")

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
                        "occupancy_rate": 95.0,
                    }
                ]
            }
        }