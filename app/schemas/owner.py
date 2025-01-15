from typing import Optional, List
from pydantic import Field, EmailStr
from app.schemas.mixins import BaseSchema
from models.owner import OwnerType, OwnerStatus


class OwnerBase(BaseSchema):
    """Base Owner Schema with common attributes"""
    name: str = Field(
        ...,
        description="Full name of the owner",
        min_length=2,
        max_length=100
    )
    owner_type: OwnerType = Field(
        default=OwnerStatus.ACTIVE,
        description="Type of owner"
    )
    status: OwnerStatus = Field(
        default=OwnerType.INDIVIDUAL,
        description="Current status of the owner"
    )
    email: EmailStr = Field(
        ...,
        description="Primary email address"
    )
    phone: str = Field(
        ...,
        description="Primary phone number",
        min_length=8,
        max_length=20
    )
    alternative_phone: Optional[str] = Field(
        default=None,
        description="Alternative phone number",
        min_length=8,
        max_length=20
    )
    address: str = Field(
        ...,
        description="Primary address",
        min_length=5,
        max_length=200
    )
    identification_number: str = Field(
        ...,
        description="Identification document number",
        max_length=50
    )
    emergency_contact_name: Optional[str] = Field(
        default=None,
        description="Emergency contact name",
        max_length=100
    )
    emergency_contact_phone: Optional[str] = Field(
        default=None,
        description="Emergency contact phone",
        max_length=20
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the owner"
    )
    telegram: Optional[str] = Field(
        default=None,
        description="Telegram number or ID"
    )
    whatsapp: Optional[str] = Field(
        default=None,
        description="Whatsapp number or ID"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "name": "John Doe",
                "owner_type": "individual",
                "status": "active",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "address": "123 Main Street, City, Country",
                "identification_type": "passport",
                "identification_number": "AB123456",
                "tags": ["resident", "primary"]
            }
        }


class OwnerCreate(OwnerBase):
    """Schema for creating a new owner"""
    pass


class OwnerUpdate(BaseSchema):
    """Schema for updating an existing owner"""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    owner_type: Optional[OwnerType] = None
    status: Optional[OwnerStatus] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=20
    )
    alternative_phone: Optional[str] = None
    alternative_address: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class OwnerInDB(OwnerBase):
    """Schema for owner as stored in database"""
    id: int = Field(..., description="Unique identifier for the owner")


class OwnerResponse(OwnerInDB):
    """Schema for owner response with additional information"""
    total_units: int = Field(
        default=0,
        description="Total number of units owned"
    )
    active_units: int = Field(
        default=0,
        description="Number of currently active units"
    )
    total_properties: int = Field(
        default=0,
        description="Total number of properties owned"
    )


class OwnerBulkCreate(BaseSchema):
    """Schema for bulk owner creation"""
    owners: List[OwnerCreate] = Field(
        description="List of owners to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "owners": [
                    {
                        "name": "John Doe",
                        "owner_type": "individual",
                        "status": "active",
                        "email": "john.doe@example.com",
                        "phone": "+1234567890",
                        "address": "123 Main Street, City, Country",
                        "identification_type": "passport",
                        "identification_number": "AB123456",
                        "tags": ["resident", "primary"]
                    }
                ]
            }
        }


class OwnerFilter(BaseSchema):
    """Schema for filtering owners"""
    owner_type: Optional[List[OwnerType]] = None
    status: Optional[List[OwnerStatus]] = None
    has_units: Optional[bool] = None
    has_active_units: Optional[bool] = None
    search: Optional[str] = Field(
        default=None,
        description="Search term for name, email, or phone"
    )
    tags: Optional[List[str]] = None


class OwnerStatistics(BaseSchema):
    """Schema for owner statistics"""
    total_owners: int = Field(..., description="Total number of owners")
    active_owners: int = Field(..., description="Number of active owners")
    total_units_owned: int = Field(..., description="Total number of units owned")
    by_type: dict = Field(..., description="Owners grouped by type")
    by_status: dict = Field(..., description="Owners grouped by status")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_owners": 100,
                "active_owners": 85,
                "total_units_owned": 150,
                "by_type": {
                    "individual": {"count": 80, "units": 100},
                    "company": {"count": 20, "units": 50}
                },
                "by_status": {
                    "active": {"count": 85, "units": 130},
                    "inactive": {"count": 15, "units": 20}
                }
            }
        }