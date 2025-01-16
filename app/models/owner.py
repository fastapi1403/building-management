from enum import Enum
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLEnum

from app.db import TableBase


# from app.models.unit import Unit
# from app.models.charge import Charge

class OwnerType(str, Enum):
    """Enumeration for owner types"""
    INDIVIDUAL = "individual"  # Individual owner
    COMPANY = "company"  # Company/Corporate owner
    TRUST = "trust"  # Trust ownership
    JOINT = "joint"  # Joint ownership
    GOVERNMENT = "government"  # Government ownership
    ASSOCIATION = "association"  # Association ownership


class OwnerStatus(str, Enum):
    """Enumeration for owner statuses"""
    ACTIVE = "active"  # Current active owner
    INACTIVE = "inactive"  # Inactive owner
    PENDING = "pending"  # Pending verification
    SUSPENDED = "suspended"  # Temporarily suspended
    BLOCKED = "blocked"  # Blocked owner
    ARCHIVED = "archived"  # Archived owner record



class Owner(TableBase):
    __tablename__ = "owners"

    owner_type: OwnerType = Field(
        sa_column=Column(SQLEnum(OwnerType)),
        default=OwnerType.INDIVIDUAL
    )
    status: OwnerStatus = Field(
        sa_column=Column(SQLEnum(OwnerStatus)),
        default=OwnerStatus.ACTIVE
    )
    name: str = Field(..., index=True)
    phone: str
    alternative_phone: Optional[str] = None
    emergency_contact_phone: Optional[str] = None
    emergency_contact_name: Optional[str] = None
    email: Optional[str] = None
    identification_number: str = Field(..., unique=True)
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    notes: Optional[str] = None

    # Relationships
    units: List["Unit"] = Relationship(back_populates="owner")
    charges: List["Charge"] = Relationship(back_populates="owner")


# Forward references for type hints
from app.models.unit import Unit
from app.models.charge import Charge