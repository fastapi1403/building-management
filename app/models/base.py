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
    deleted: bool = Field(
        default=False,
        index=True
    )
    deleted_at: Optional[datetime] = Field(
        default=None,
        nullable=True,
        index=True
    )

    @model_validator(mode='before')
    def update_timestamps(cls, values):
        values['updated_at'] = datetime.now(UTC)
        return values

class SoftDeleteMixin:
    @classmethod
    async def soft_delete(cls, db, model_id: int) -> bool:
        try:
            obj = await db.get(cls, model_id)
            if obj:
                obj.deleted_at = datetime.now(UTC)
                db.add(obj)
                await db.commit()
                logger.info(f"{cls.__name__} with ID {model_id} soft deleted")
                return True
            return False
        except Exception as e:
            logger.error(f"Error soft deleting {cls.__name__} with ID {model_id}: {str(e)}")
            raise

class AuditMixin:
    @classmethod
    def log_change(cls, action: str, instance_id: int, data: dict):
        logger.info(
            f"{action} {cls.__name__} | ID: {instance_id} | "
            f"Data: {data} | Time: {datetime.now(UTC)}"
        )