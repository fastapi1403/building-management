from datetime import datetime, UTC
from typing import Optional
from sqlmodel import SQLModel, Field
from pydantic import field_validator, model_validator
from loguru import logger

class TimestampMixin(SQLModel):
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        index=True
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        nullable=False,
        index=True
    )

    @model_validator(mode='before')
    def update_timestamps(cls, values):
        values['updated_at'] = datetime.now(UTC)
        return values

class SoftDeleteMixin(SQLModel):
    is_deleted: bool = Field(
        default=False,
        index=True
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
    )

    def soft_delete(self) -> None:
        """Soft delete the record"""
        self.deleted_at = datetime.now(UTC)
        self.is_deleted = True

    def restore(self) -> None:
        """Restore the soft deleted record"""
        self.deleted_at = None
        self.is_deleted = False