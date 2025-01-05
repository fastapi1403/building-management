from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlmodel import SQLModel

@as_declarative()
class Base(SQLModel):
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -
        return cls.__name__.lower()
