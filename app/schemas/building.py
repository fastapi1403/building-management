from typing import Optional, List
from pydantic import BaseModel, Field
from .base import TimestampSchema

class BuildingBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    address: str = Field(..., min_length=5, max_length=200)
    city: str = Field(..., min_length=2, max_length=100)
    postal_code: str = Field(..., min_length=5, max_length=10)
    country: str = Field(default="India", min_length=2, max_length=100)
    total_floors: int = Field(..., gt=0)
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Crystal Tower",
                "address": "123 Main Street, Bandra West",
                "city": "Mumbai",
                "postal_code": "400050",
                "country": "India",
                "total_floors": 15,
                "description": "Luxury residential building with modern amenities"
            }
        }


class BuildingCreate(BuildingBase):
    pass

class BuildingUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    address: Optional[str] = Field(None, min_length=5, max_length=200)
    city: Optional[str] = Field(None, min_length=2, max_length=100)
    postal_code: Optional[str] = Field(None, min_length=5, max_length=10)
    total_floors: Optional[int] = Field(None, gt=0)
    description: Optional[str] = Field(None, max_length=500)

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Crystal Tower Updated",
                "address": "123 Main Street, Bandra West",
                "city": "Mumbai",
                "postal_code": "400050",
                "total_floors": 20,
                "description": "Updated luxury residential building description"
            }
        }


class BuildingResponse(BuildingBase, TimestampSchema):
    id: int

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Crystal Tower",
                "address": "123 Main Street, Bandra West",
                "city": "Mumbai",
                "postal_code": "400050",
                "country": "India",
                "total_floors": 15,
                "description": "Luxury residential building with modern amenities",
                "created_at": "2025-01-15T08:42:00Z",
                "updated_at": "2025-01-15T08:42:00Z",
                "deleted_at": None
            }
        }
