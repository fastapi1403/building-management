from datetime import datetime
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base_class import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD object with default methods to Create, Read, Update, Delete (CRUD).

        Args:
            model: A SQLAlchemy model class
        """
        self.model = model

    async def get(
            self,
            db: AsyncSession,
            id: Any
    ) -> Optional[ModelType]:
        """
        Get a record by ID.
        """
        query = select(self.model).filter(self.model.id == id)
        result = await db.execute(query)
        return result.scalar_one_or_none()

    async def get_multi(
            self,
            db: AsyncSession,
            *,
            skip: int = 0,
            limit: int = 100
    ) -> List[ModelType]:
        """
        Get multiple records.
        """
        query = select(self.model).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create(
            self,
            db: AsyncSession,
            *,
            obj_in: CreateSchemaType,
            created_by: str = "fastapi1403"  # Default to current user
    ) -> ModelType:
        """
        Create new record.
        """
        obj_in_data = obj_in.model_dump()
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # Add audit fields
        obj_in_data.update({
            "created_at": current_time,
            "created_by": created_by,
            "updated_at": current_time,
            "updated_by": created_by,
            "is_deleted": False
        })

        db_obj = self.model(**obj_in_data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]],
            updated_by: str = "fastapi1403"  # Default to current user
    ) -> ModelType:
        """
        Update existing record.
        """
        obj_data = db_obj.__dict__

        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        # Add audit fields
        update_data.update({
            "updated_at": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S"),
            "updated_by": updated_by
        })

        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            deleted_by: str = "fastapi1403"  # Default to current user
    ) -> ModelType:
        """
        Soft delete record.
        """
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        setattr(db_obj, "is_deleted", True)
        setattr(db_obj, "deleted_at", current_time)
        setattr(db_obj, "deleted_by", deleted_by)
        setattr(db_obj, "updated_at", current_time)
        setattr(db_obj, "updated_by", deleted_by)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def restore(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            restored_by: str = "fastapi1403"  # Default to current user
    ) -> ModelType:
        """
        Restore soft-deleted record.
        """
        current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        setattr(db_obj, "is_deleted", False)
        setattr(db_obj, "deleted_at", None)
        setattr(db_obj, "deleted_by", None)
        setattr(db_obj, "updated_at", current_time)
        setattr(db_obj, "updated_by", restored_by)

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def hard_delete(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType
    ) -> None:
        """
        Hard delete record.
        """
        await db.delete(db_obj)
        await db.commit()

    async def count(
            self,
            db: AsyncSession,
            *,
            include_deleted: bool = False
    ) -> int:
        """
        Count total records.
        """
        query = select(self.model)
        if not include_deleted:
            query = query.filter(self.model.is_deleted == False)
        result = await db.execute(query)
        return len(result.scalars().all())

    async def exists(
            self,
            db: AsyncSession,
            id: Any
    ) -> bool:
        """
        Check if record exists by ID.
        """
        query = select(self.model).filter(
            self.model.id == id,
            self.model.is_deleted == False
        )
        result = await db.execute(query)
        return result.scalar_one_or_none() is not None