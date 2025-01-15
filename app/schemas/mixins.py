# app/schemas/mixins.py
from datetime import datetime, UTC
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict

class TimestampMixinSchema(BaseModel):
    """Schema mixin for timestamp fields"""
    model_config = ConfigDict(
        from_attributes=True,  # Allow ORM model conversion
        json_encoders={datetime: lambda dt: dt.isoformat()},  # Format datetime
    )

    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Record creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="Record last update timestamp"
    )
    created_by: str = Field(
        default="fastapi1403",
        description="User who created the record"
    )
    updated_by: str = Field(
        default="fastapi1403",
        description="User who last updated the record"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "created_at": "2025-01-15T14:08:30Z",
                "updated_at": "2025-01-15T14:08:30Z",
                "created_by": "fastapi1403",
                "updated_by": "fastapi1403"
            }
        }


class SoftDeleteMixinSchema(BaseModel):
    """Schema mixin for soft delete fields"""
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={datetime: lambda dt: dt.isoformat()}
    )

    deleted_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp when the record was soft deleted"
    )
    is_deleted: bool = Field(
        default=False,
        description="Indicates if the record is soft deleted"
    )
    deleted_by: Optional[str] = Field(
        default=None,
        description="User who soft deleted the record"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "deleted_at": None,
                "is_deleted": False,
                "deleted_by": None
            }
        }


# Example of combined base schema
class BaseSchema(TimestampMixinSchema, SoftDeleteMixinSchema):
    """Base schema with both timestamp and soft delete functionality"""
    id: Optional[int] = Field(default=None, description="Primary key")

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "created_at": "2025-01-15T14:08:30Z",
                "updated_at": "2025-01-15T14:08:30Z",
                "created_by": "fastapi1403",
                "updated_by": "fastapi1403",
                "deleted_at": None,
                "is_deleted": False,
                "deleted_by": None
            }
        }