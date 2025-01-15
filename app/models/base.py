from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import validator, field_validator, model_validator


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

    # Using model_validator instead of field_validator for this case
    @model_validator(mode='before')
    def set_updated_at(cls, values):
        values['updated_at'] = datetime.now(UTC)
        return values
