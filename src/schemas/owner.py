from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from .base import BaseSchema

class OwnerBase(BaseSchema):
    name: str = Field(..., description="Owner's full name")
    email: EmailStr = Field(..., description="Owner's email address")
    phone: str = Field(..., description="Owner's phone number")
    national_id: str = Field(..., description="Owner's national ID")

class OwnerCreate(OwnerBase):
    password: str = Field(..., description="Owner's password")

class OwnerUpdate(BaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class OwnerRead(OwnerBase):
    id: int
    created_at: datetime
    updated_at: datetime

class OwnerInDB(OwnerRead):
    hashed_password: str
