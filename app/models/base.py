from datetime import datetime
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator

class TimestampModel(SQLModel):
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    deleted_at: Optional[datetime] = Field(default=None)

    @validator("updated_at", always=True)
    def set_updated_at(cls, v, values):
        return datetime.utcnow()
