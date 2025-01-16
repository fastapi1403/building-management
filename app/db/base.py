from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import ConfigDict


class TableBase(SQLModel):
    """
    Base class for all models using SQLModel.
    Provides common fields and functionality for audit trails.
    """

    model_config = ConfigDict(
        from_attributes=True,
        arbitrary_types_allowed = True,
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%d %H:%M:%S")
        },
        json_schema_extra={
            "example": {
                "id": 1,
                "created_at": "2025-01-16 14:14:34",
                "updated_at": "2025-01-16 14:14:34",
            }
        }
    )

    id: Optional[int] = Field(default=None, primary_key=True)

    # Audit trail fields
    created_at: datetime = Field(
        default_factory=lambda: datetime.strptime(
            "2025-01-16 14:14:34",
            "%Y-%m-%d %H:%M:%S"
        ),
        nullable=False
    )

    updated_at: datetime = Field(
        default_factory=lambda: datetime.strptime(
            "2025-01-16 14:14:34",
            "%Y-%m-%d %H:%M:%S"
        ),
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
        current_time = datetime.strptime(
            "2025-01-16 14:14:34",
            "%Y-%m-%d %H:%M:%S"
        )

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        self.updated_at = current_time

    def soft_delete(self) -> None:
        """
        Soft delete the record
        Sets is_deleted flag and updates audit trail
        """
        current_time = datetime.strptime(
            "2025-01-16 14:14:34",
            "%Y-%m-%d %H:%M:%S"
        )

        self.is_deleted = True
        self.deleted_at = current_time
        self.updated_at = current_time

    def restore(self) -> None:
        """
        Restore a soft-deleted record
        Clears deletion flags and updates audit trail
        """
        current_time = datetime.strptime(
            "2025-01-16 14:14:34",
            "%Y-%m-%d %H:%M:%S"
        )

        self.is_deleted = False
        self.deleted_at = None
        self.updated_at = current_time


# Create table=False models base class
class SchemaBase(TableBase, table=False):
    """
    Base class for SQLModel schema models (Pydantic models)
    Inherit from this class for request/response schemas
    """
    pass