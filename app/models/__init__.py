from .mixins import TimestampModel
from .building import Building
from .floor import Floor
from .unit import Unit
from .owner import Owner
from .tenant import Tenant

__all__ = [
    "TimestampModel", "Building", "Floor", "Unit", "Owner", "Tenant"
]

# from datetime import datetime
# from typing import Any
# from sqlalchemy.ext.declarative import as_declarative, declared_attr
# from sqlalchemy import Column, DateTime
#
#
# @as_declarative()
# class Base:
#     id: Any
#     __name__: str
#
#     @declared_attr
#     def __tablename__(cls) -> str:
#         return cls.__name__.lower()
#
#     created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
#     updated_at = Column(
#         DateTime,
#         default=datetime.utcnow,
#         onupdate=datetime.utcnow,
#         nullable=False
#     )
#
#
# from datetime import datetime
# from typing import Optional
# from sqlmodel import SQLModel, Field
#
#
# class TimeStampModel(SQLModel):
#     created_at: datetime = Field(default_factory=datetime.utcnow)
#     updated_at: datetime = Field(default_factory=datetime.utcnow)
#     deleted_at: Optional[datetime] = Field(default=None, index=True)
