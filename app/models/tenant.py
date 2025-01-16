from datetime import date
from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLEnum

from app.models.mixins import SoftDeleteMixin, TimestampMixin
# from mixins import TimestampMixin, SoftDeleteMixin
# from app.models.unit import Unit
# from app.models.charge import Charge

class TenantType(str, Enum):
    """Enumeration for tenant types"""
    INDIVIDUAL = "individual"  # Individual tenant
    FAMILY = "family"  # Family tenant
    COMPANY = "company"  # Corporate tenant
    STUDENT = "student"  # Student tenant
    GOVERNMENT = "government"  # Government tenant
    ORGANIZATION = "organization"  # Organization tenant


class TenantStatus(str, Enum):
    """Enumeration for tenant statuses"""
    ACTIVE = "active"  # Currently active tenant
    INACTIVE = "inactive"  # Inactive tenant
    PENDING = "pending"  # Pending verification
    SUSPENDED = "suspended"  # Temporarily suspended
    NOTICE_GIVEN = "notice_given"  # Given notice to leave
    MOVED_OUT = "moved_out"  # Former tenant
    EVICTED = "evicted"  # Evicted tenant
    BLACKLISTED = "blacklisted"  # Blacklisted tenant


class Tenant(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "tenants"

    id: Optional[int] = Field(default=None, primary_key=True)
    unit_id: int = Field(foreign_key="units.id")
    tenant_type: TenantType = Field(
        sa_column=Column(SQLEnum(TenantType)),
        default=TenantType.INDIVIDUAL
    )
    status: TenantStatus = Field(
        sa_column=Column(SQLEnum(TenantStatus)),
        default=TenantStatus.ACTIVE
    )

    name: str = Field(..., index=True)
    phone: str
    emergency_contact_phone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    emergency_contact_relation: Optional[str] = None
    notes: Optional[str] = None
    vehicle_info: Optional[str] = None
    email: Optional[str] = None
    identification_number: str = Field(..., unique=True)
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    occupant_count: int = Field(default=1)
    lease_start_date: date
    lease_end_date: date

    # Relationships
    unit: "Unit" = Relationship(back_populates="tenant")
    charges: List["Charge"] = Relationship(back_populates="tenant")


Tenant.model_rebuild()