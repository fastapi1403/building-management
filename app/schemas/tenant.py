from typing import Optional
from datetime import date
from pydantic import BaseModel, Field, EmailStr
from .mixins import TimestampSchema

class TenantBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    lease_start_date: date
    lease_end_date: date
    unit_id: int

    @field_validator('lease_end_date')
    @classmethod
    def validate_lease_dates(cls, v, values):
        start_date = values.data.get('lease_start_date')
        if start_date and v <= start_date:
            raise ValueError('lease_end_date must be after lease_start_date')
        return v

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None

class TenantResponse(TenantBase, TimestampSchema):
    id: int

# from typing import Optional
# from pydantic import BaseModel, Field, EmailStr
# from .base import TimeStampSchema
#
#
# class TenantBase(BaseModel):
#     unit_id: int = Field(..., description="ID of the unit")
#     name: str = Field(..., min_length=2, description="Full name of the tenant")
#     phone: str = Field(..., description="Contact phone number")
#     email: Optional[EmailStr] = Field(None, description="Email address")
#     national_id: str = Field(..., description="National ID number")
#     whatsapp: Optional[str] = Field(None, description="WhatsApp number")
#     telegram: Optional[str] = Field(None, description="Telegram handle")
#     occupant_count: int = Field(default=1, ge=1, description="Number of occupants")
#
#
# class TenantCreate(TenantBase):
#     pass
#
#
# class TenantUpdate(TenantBase):
#     unit_id: Optional[int] = None
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     occupant_count: Optional[int] = None
#
#
# class Tenant(TenantBase, TimeStampSchema):
#     id: int
#
#
# class TenantDetail(Tenant):
#     total_charges: float
#     unpaid_charges: float
#
# # --------------------
#
# from typing import Optional
# from pydantic import Field, EmailStr
# from . import BaseSchema, TimeStampSchema
#
#
# class TenantBase(BaseSchema):
#     unit_id: int = Field(..., description="ID of the unit")
#     name: str = Field(..., min_length=2, description="Full name of the tenant")
#     phone: str = Field(..., description="Contact phone number")
#     email: Optional[EmailStr] = Field(None, description="Email address")
#     national_id: str = Field(..., description="National ID number")
#     whatsapp: Optional[str] = Field(None, description="WhatsApp number")
#     telegram: Optional[str] = Field(None, description="Telegram handle")
#     occupant_count: int = Field(default=1, ge=1, description="Number of occupants")
#
#
# class TenantCreate(TenantBase):
#     pass
#
#
# class TenantUpdate(TenantBase):
#     unit_id: Optional[int] = None
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     occupant_count: Optional[int] = None
#
#
# class Tenant(TenantBase, TimeStampSchema):
#     id: int