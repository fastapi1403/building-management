from datetime import datetime
from typing import Optional, List
from pydantic import Field, EmailStr
from app.schemas.mixins import BaseSchema
from models.tenant import TenantType, TenantStatus


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
    current_address: str = Field(
        ...,
        description="Current residence address",
        min_length=5,
        max_length=200
    )
    identification_number: str = Field(
        ...,
        description="Identification document number",
        max_length=50
    )
    lease_start_date: Optional[datetime] = Field(
        default=None,
        description="Start date of the lease"
    )
    lease_end_date: Optional[datetime] = Field(
        default=None,
        description="End date of the lease"
    )
    unit_id: Optional[int] = Field(
        default=None,
        description="ID of the unit being rented"
    )
    building_id: Optional[int] = Field(
        default=None,
        description="ID of the building"
    )
    emergency_contact_name: str = Field(
        ...,
        description="Emergency contact name",
        max_length=100
    )
    emergency_contact_phone: str = Field(
        ...,
        description="Emergency contact phone",
        max_length=20
    )
    emergency_contact_relation: str = Field(
        ...,
        description="Relationship with emergency contact",
        max_length=50
    )
    vehicle_info: Optional[str] = Field(
        default=None,
        description="Vehicle information if any",
        max_length=200
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the tenant"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "name": "Jane Smith",
                "tenant_type": "individual",
                "status": "active",
                "email": "jane.smith@example.com",
                "phone": "+1234567890",
                "current_address": "Unit 501, Building A, 123 Main Street",
                "identification_type": "driver_license",
                "identification_number": "DL123456789",
                "lease_start_date": "2025-01-15 15:13:55",
                "lease_end_date": "2026-01-15 15:13:55",
                "unit_id": 501,
                "building_id": 1,
                "emergency_contact_name": "John Smith",
                "emergency_contact_phone": "+1987654321",
                "emergency_contact_relation": "spouse",
                "occupation": "Software Engineer",
                "employer": "Tech Corp",
                "tags": ["long_term", "professional"]
            }
        }


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
    phone: Optional[str] = None
    alternative_phone: Optional[str] = None
    current_address: Optional[str] = None
    permanent_address: Optional[str] = None
    lease_start_date: Optional[datetime] = None
    lease_end_date: Optional[datetime] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    occupation: Optional[str] = None
    employer: Optional[str] = None
    employer_phone: Optional[str] = None
    vehicle_info: Optional[str] = None
    notes: Optional[str] = None


class TenantInDB(TenantBase):
    """Schema for tenant as stored in database"""
    id: int = Field(..., description="Unique identifier for the tenant")


class TenantResponse(TenantInDB):
    """Schema for tenant response"""
    lease_duration: Optional[int] = Field(
        default=None,
        description="Duration of lease in months"
    )
    remaining_lease_days: Optional[int] = Field(
        default=None,
        description="Remaining days in current lease"
    )
    payment_history: Optional[dict] = Field(
        default=None,
        description="Summary of payment history"
    )


class TenantBulkCreate(BaseSchema):
    """Schema for bulk tenant creation"""
    tenants: List[TenantCreate] = Field(
        description="List of tenants to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "tenants": [{
                    "name": "Jane Smith",
                    "tenant_type": "individual",
                    "status": "active",
                    "email": "jane.smith@example.com",
                    "phone": "+1234567890",
                    "current_address": "Unit 501, Building A",
                    "identification_type": "driver_license",
                    "identification_number": "DL123456789",
                    "lease_start_date": "2025-01-15 15:13:55",
                    "unit_id": 501,
                    "building_id": 1,
                    "emergency_contact_name": "John Smith",
                    "emergency_contact_phone": "+1987654321",
                    "emergency_contact_relation": "spouse"
                }]
            }
        }


class TenantFilter(BaseSchema):
    """Schema for filtering tenants"""
    building_id: Optional[int] = None
    unit_id: Optional[int] = None
    tenant_type: Optional[List[TenantType]] = None
    status: Optional[List[TenantStatus]] = None
    lease_expiring_in_days: Optional[int] = None
    search: Optional[str] = Field(
        default=None,
        description="Search term for name, email, or phone"
    )
    tags: Optional[List[str]] = None


class TenantStatistics(BaseSchema):
    """Schema for tenant statistics"""
    total_tenants: int = Field(..., description="Total number of tenants")
    active_tenants: int = Field(..., description="Number of active tenants")
    pending_tenants: int = Field(..., description="Number of pending tenants")
    expiring_leases: int = Field(..., description="Number of leases expiring in 30 days")
    by_type: dict = Field(..., description="Tenants grouped by type")
    by_status: dict = Field(..., description="Tenants grouped by status")
    occupancy_rate: float = Field(..., description="Overall occupancy rate")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_tenants": 150,
                "active_tenants": 120,
                "pending_tenants": 15,
                "expiring_leases": 8,
                "by_type": {
                    "individual": {"count": 100, "percentage": 66.67},
                    "family": {"count": 50, "percentage": 33.33}
                },
                "by_status": {
                    "active": {"count": 120, "percentage": 80.0},
                    "pending": {"count": 15, "percentage": 10.0},
                    "notice_given": {"count": 15, "percentage": 10.0}
                },
                "occupancy_rate": 85.5
            }
        }