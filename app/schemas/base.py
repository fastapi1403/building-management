from models.base import Base


# Create table=False models base class
class SchemaBase(Base, table=False):
    """
    Base class for SQLModel schema models (Pydantic models)
    Inherit from this class for request/response schemas
    """
    pass
