from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr

class TimestampSchema(BaseModel):
    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime] = None

    class Config:
        from_attributes = True  # New in Pydantic v2, replaces orm_mode
        json_schema_extra = {
            "example": {
                "created_at": "2025-01-15T08:42:00Z",
                "updated_at": "2025-01-15T08:42:00Z",
                "deleted_at": None
            }
        }