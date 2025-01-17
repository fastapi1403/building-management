from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field

# Create table=False models base class
class SchemaBase(SQLModel, table=False):
    """
    Base class for SQLModel schema models (Pydantic models).
    Inherit from this class for request/response schemas.

    This class is used to define Pydantic models that do not map to database tables directly.
    It is useful for defining schemas for request and response data structures.
    """

    id: Optional[int] = Field(None, description="Unique identifier for the record")
    created_at: Optional[datetime] = Field(default=None, description="Date and time when the record was created")
    updated_at: Optional[datetime] = Field(default=None, description="Date and time when the record was last updated")
    is_deleted: Optional[bool] = Field(default=False, description="Indicates if the record is deleted")
    deleted_at: Optional[datetime] = Field(None, description="Date and time when the record was deleted")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2025-01-16T15:55:47",
                "updated_at": "2025-01-17T15:55:47",
                "is_deleted": False,
                "deleted_at": None,
            }
        }