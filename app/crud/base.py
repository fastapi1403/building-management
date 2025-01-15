from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.base import Base
from app.utils.logger import log

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: AsyncSession, id: Any) -> Optional[ModelType]:
        try:
            query = select(self.model).where(self.model.id == id)
            result = await db.execute(query)
            return result.scalar_one_or_none()
        except Exception as e:
            log.error(f"Error retrieving {self.model.__name__} with id {id}: {str(e)}")
            raise

    async def get_multi(
            self, db: AsyncSession, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        try:
            query = select(self.model).offset(skip).limit(limit)
            result = await db.execute(query)
            return result.scalars().all()
        except Exception as e:
            log.error(f"Error retrieving multiple {self.model.__name__}: {str(e)}")
            raise

    async def create(self, db: AsyncSession, *, obj_in: CreateSchemaType) -> ModelType:
        try:
            obj_in_data = jsonable_encoder(obj_in)
            db_obj = self.model(**obj_in_data)
            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            log.info(f"Created new {self.model.__name__} with id {db_obj.id}")
            return db_obj
        except Exception as e:
            await db.rollback()
            log.error(f"Error creating {self.model.__name__}: {str(e)}")
            raise

    async def update(
            self,
            db: AsyncSession,
            *,
            db_obj: ModelType,
            obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        try:
            obj_data = jsonable_encoder(db_obj)
            if isinstance(obj_in, dict):
                update_data = obj_in
            else:
                update_data = obj_in.dict(exclude_unset=True)

            for field in obj_data:
                if field in update_data:
                    setattr(db_obj, field, update_data[field])

            db.add(db_obj)
            await db.commit()
            await db.refresh(db_obj)
            log.info(f"Updated {self.model.__name__} with id {db_obj.id}")
            return db_obj
        except Exception as e:
            await db.rollback()
            log.error(f"Error updating {self.model.__name__} with id {db_obj.id}: {str(e)}")
            raise

    async def delete(self, db: AsyncSession, *, id: int) -> ModelType:
        try:
            obj = await self.get(db, id)
            await db.delete(obj)
            await db.commit()
            log.info(f"Deleted {self.model.__name__} with id {id}")
            return obj
        except Exception as e:
            await db.rollback()
            log.error(f"Error deleting {self.model.__name__} with id {id}: {str(e)}")
            raise