from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field
from .base import BaseSchema

class TenantBase(BaseSchema):
    name: str = Field(..., description="Tenant's full name")
    email: EmailStr = Field(..., description="Tenant's email address")
    phone: str = Field(..., description="Tenant's phone number")
    national_id: str = Field(..., description="Tenant's national ID")
    unit_id: int = Field(..., description="ID of the rented unit")

class TenantCreate(TenantBase):
    password: str = Field(..., description="Tenant's password")

class TenantUpdate(BaseSchema):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    password: Optional[str] = None

class TenantRead(TenantBase):
    id: int
    created_at: datetime
    updated_at: datetime

class TenantInDB(TenantRead):
    hashed_password: str
