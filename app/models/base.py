from datetime import datetime, timezone
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class Base(SQLModel):
    """
    Base class for all models using SQLModel.
    Provides common fields and functionality for audit trails.
    """

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed = True,
        json_encoders = {
            datetime: lambda dt: dt.isoformat()
        },
        json_schema_extra={
            "example": {
                "id": 1,
                "created_at": "2025-01-16T14:14:34+00:00",
                "updated_at": "2025-01-16T14:14:34+00:00",
            }
        }
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # Audit trail fields
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False
    )

    # Soft delete fields
    is_deleted: bool = Field(
        default=False,
        index=True,
        nullable=False
    )

    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True
    )

    def update(self, **kwargs) -> None:
        """
        Update model instance with provided values
        Updates audit trail automatically
        """
        current_time = datetime.now(timezone.utc)

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = current_time

    def soft_delete(self) -> None:
        """
        Soft delete the record
        Sets is_deleted flag and updates audit trail
        """
        current_time = datetime.now(timezone.utc)

        self.is_deleted = True
        self.deleted_at = current_time
        self.updated_at = current_time

    def restore(self) -> None:
        """
        Restore a soft-deleted record
        Clears deletion flags and updates audit trail
        """
        current_time = datetime.now(timezone.utc)

        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = current_time


# Create table=False models base class
class TableBase(Base, table=False):
    """
    Base class for SQLModel table models
    Inherit from this class for database models
    """
    pass



