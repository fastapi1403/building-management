from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr
from .mixins import TimestampSchema

class OwnerBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(..., min_length=10, max_length=15)
    address: Optional[str] = Field(None, max_length=200)

class OwnerCreate(OwnerBase):
    pass

class OwnerUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, min_length=10, max_length=15)
    address: Optional[str] = Field(None, max_length=200)

class OwnerResponse(OwnerBase, TimestampSchema):
    id: int

# from typing import Optional, List
# from pydantic import BaseModel, Field, EmailStr
# from .base import TimeStampSchema
#
#
# class OwnerBase(BaseModel):
#     name: str = Field(..., min_length=2, description="Full name of the owner")
#     phone: str = Field(..., description="Contact phone number")
#     email: Optional[EmailStr] = Field(None, description="Email address")
#     national_id: str = Field(..., description="National ID number")
#     whatsapp: Optional[str] = Field(None, description="WhatsApp number")
#     telegram: Optional[str] = Field(None, description="Telegram handle")
#
#
# class OwnerCreate(OwnerBase):
#     pass
#
#
# class OwnerUpdate(OwnerBase):
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     email: Optional[EmailStr] = None
#     national_id: Optional[str] = None
#
#
# class Owner(OwnerBase, TimeStampSchema):
#     id: int
#
#
# class OwnerDetail(Owner):
#     units: List["UnitBase"]
#     total_charges: float
#     unpaid_charges: float
#
# # -----------------------------
#
# from typing import Optional, List
# from pydantic import Field, EmailStr
# from . import BaseSchema, TimeStampSchema
#
#
# class OwnerBase(BaseSchema):
#     name: str = Field(..., min_length=2, description="Full name of the owner")
#     phone: str = Field(..., description="Contact phone number")
#     email: Optional[EmailStr] = Field(None, description="Email address")
#     national_id: str = Field(..., description="National ID number")
#     whatsapp: Optional[str] = Field(None, description="WhatsApp number")
#     telegram: Optional[str] = Field(None, description="Telegram handle")
#
#
# class OwnerCreate(OwnerBase):
#     pass
#
#
# class OwnerUpdate(OwnerBase):
#     name: Optional[str] = None
#     phone: Optional[str] = None
#     national_id: Optional[str] = None
#
#
# class Owner(OwnerBase, TimeStampSchema):
#     id: int