from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator, field_validator


class TimestampModel(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),  # Changed from utcnow() to now(UTC)
        nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),  # Changed from utcnow() to now(UTC)
        nullable=False
    )
    deleted_at: Optional[datetime] = Field(default=None)

    @field_validator("updated_at", mode="before")
    @classmethod
    def set_updated_at(cls, v, info):
        return datetime.now(UTC)  # Changed from utcnow() to now(UTC)
