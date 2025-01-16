from datetime import date
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLEnum
from app.models.base import TableBase

# Enumeration for tenant types
class TenantType(str, Enum):
    INDIVIDUAL = "individual"  # Individual tenant
    FAMILY = "family"  # Family tenant
    COMPANY = "company"  # Corporate tenant
    STUDENT = "student"  # Student tenant
    GOVERNMENT = "government"  # Government tenant
    ORGANIZATION = "organization"  # Organization tenant

# Enumeration for tenant statuses
class TenantStatus(str, Enum):
    ACTIVE = "active"  # Currently active tenant
    INACTIVE = "inactive"  # Inactive tenant
    PENDING = "pending"  # Pending verification
    SUSPENDED = "suspended"  # Temporarily suspended
    NOTICE_GIVEN = "notice_given"  # Given notice to leave
    MOVED_OUT = "moved_out"  # Former tenant
    EVICTED = "evicted"  # Evicted tenant
    BLACKLISTED = "blacklisted"  # Blacklisted tenant

# Model for representing a tenant in the building management system
class Tenant(TableBase, table=True):
    __tablename__ = "tenants"
    __table_args__ = {'extend_existing': True}

    unit_id: int = Field(foreign_key="units.id", description="ID of the associated unit")
    tenant_type: TenantType = Field(
        sa_column=Column(SQLEnum(TenantType)),
        default=TenantType.INDIVIDUAL,
        description="Type of tenant"
    )
    status: TenantStatus = Field(
        sa_column=Column(SQLEnum(TenantStatus)),
        default=TenantStatus.ACTIVE,
        description="Status of the tenant"
    )

    name: str = Field(..., index=True, description="Name of the tenant")
    phone: str = Field(..., description="Primary phone number of the tenant")
    emergency_contact_phone: Optional[str] = Field(default=None, description="Emergency contact phone number")
    emergency_contact_name: Optional[str] = Field(default=None, description="Emergency contact name")
    emergency_contact_relation: Optional[str] = Field(default=None, description="Relation to emergency contact")
    notes: Optional[str] = Field(default=None, description="Additional notes about the tenant")
    vehicle_info: Optional[str] = Field(default=None, description="Information about the tenant's vehicle")
    email: Optional[str] = Field(default=None, description="Email address of the tenant")
    identification_number: str = Field(..., unique=True, description="Unique identification number")
    whatsapp: Optional[str] = Field(default=None, description="WhatsApp contact")
    telegram: Optional[str] = Field(default=None, description="Telegram contact")
    occupant_count: int = Field(default=1, description="Number of occupants in the unit")
    lease_start_date: date = Field(..., description="Start date of the lease")
    lease_end_date: date = Field(..., description="End date of the lease")

    # Relationships
    unit: "Unit" = Relationship(back_populates="tenant")
    charges: List["Charge"] = Relationship(back_populates="tenant")

    class Config:
        json_schema_extra = {
            "example": {
                "unit_id": 1,
                "tenant_type": "individual",
                "status": "active",
                "name": "Alice Johnson",
                "phone": "+1234567890",
                "emergency_contact_phone": "+0987654321",
                "emergency_contact_name": "Bob Johnson",
                "emergency_contact_relation": "Spouse",
                "notes": "Allergic to pets",
                "vehicle_info": "Red Toyota Camry, License Plate ABC123",
                "email": "alice.johnson@example.com",
                "identification_number": "ID987654321",
                "whatsapp": "+1234567890",
                "telegram": "@alicejohnson",
                "occupant_count": 3,
                "lease_start_date": "2025-01-01",
                "lease_end_date": "2025-12-31"
            }
        }

# Forward references for type hints
from app.models.unit import Unit
from app.models.charge import Charge