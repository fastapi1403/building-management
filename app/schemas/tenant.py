from typing import Optional, List
from datetime import date
from pydantic import Field, EmailStr, ConfigDict
from app.schemas.mixins import BaseSchema
from app.models.tenant import TenantType, TenantStatus


class TenantBase(BaseSchema):
    """Base Tenant Schema with common attributes"""
    name: str = Field(
        ...,
        description="Full name of the tenant",
        min_length=2,
        max_length=100
    )
    tenant_type: TenantType = Field(
        default=TenantType.INDIVIDUAL,
        description="Type of tenant"
    )
    status: TenantStatus = Field(
        default=TenantStatus.ACTIVE,
        description="Current status of the tenant"
    )
    email: Optional[EmailStr] = Field(
        default=None,
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
    identification_number: Optional[str] = Field(
        default=None,
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
    occupation: Optional[str] = Field(
        default=None,
        description="Tenant's occupation"
    )
    employer: Optional[str] = Field(
        default=None,
        description="Tenant's employer"
    )
    contract_start_date: Optional[date] = Field(
        default=None,
        description="Start date of the tenancy contract"
    )
    contract_end_date: Optional[date] = Field(
        default=None,
        description="End date of the tenancy contract"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the tenant"
    )
    telegram: Optional[str] = Field(
        default=None,
        description="Telegram number or ID"
    )
    whatsapp: Optional[str] = Field(
        default=None,
        description="Whatsapp number or ID"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "name": "John Doe",
                "tenant_type": "individual",
                "status": "active",
                "email": "john.doe@example.com",
                "phone": "+1234567890",
                "address": "123 Main Street, City, Country",
                "identification_number": "AB123456",
                "occupation": "Software Engineer",
                "contract_start_date": "2024-01-01",
                "contract_end_date": "2024-12-31"
            }
        }
    )


class TenantCreate(TenantBase):
    """Schema for creating a new tenant"""
    pass


class TenantUpdate(BaseSchema):
    """Schema for updating an existing tenant"""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    tenant_type: Optional[TenantType] = None
    status: Optional[TenantStatus] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(
        default=None,
        min_length=8,
        max_length=20
    )
    alternative_phone: Optional[str] = None
    identification_number: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    lease_start_date: Optional[date] = None
    lease_end_date: Optional[date] = None
    notes: Optional[str] = None


class TenantInDB(TenantBase):
    """Schema for tenant as stored in database"""
    id: int = Field(..., description="Unique identifier for the tenant")


class TenantResponse(TenantInDB):
    """Schema for tenant response with additional information"""
    total_units: int = Field(
        default=0,
        description="Total number of units rented"
    )
    active_units: int = Field(
        default=0,
        description="Number of currently active rental units"
    )


class TenantBulkCreate(BaseSchema):
    """Schema for bulk tenant creation"""
    tenants: List[TenantCreate] = Field(
        description="List of tenants to create",
        min_length=1
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "tenants": [
                    {
                        "name": "John Doe",
                        "tenant_type": "individual",
                        "status": "active",
                        "email": "john.doe@example.com",
                        "phone": "+1234567890",
                        "address": "123 Main Street, City, Country",
                        "identification_number": "AB123456",
                        "occupation": "Software Engineer",
                        "contract_start_date": "2024-01-01",
                        "contract_end_date": "2024-12-31"
                    }
                ]
            }
        }
    )


class TenantFilter(BaseSchema):
    """Schema for filtering tenants"""
    tenant_type: Optional[List[TenantType]] = None
    status: Optional[List[TenantStatus]] = None
    has_units: Optional[bool] = None
    has_active_units: Optional[bool] = None
    search: Optional[str] = Field(
        default=None,
        description="Search term for name, email, or phone"
    )


class TenantStatistics(BaseSchema):
    """Schema for tenant statistics"""
    total_tenants: int = Field(..., description="Total number of tenants")
    active_tenants: int = Field(..., description="Number of active tenants")
    total_units_rented: int = Field(..., description="Total number of units rented")
    by_type: dict = Field(..., description="Tenants grouped by type")
    by_status: dict = Field(..., description="Tenants grouped by status")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_tenants": 100,
                "active_tenants": 85,
                "total_units_rented": 150,
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
    )