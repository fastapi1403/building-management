from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, Relationship

from app.models.base import TableBase


# Enumeration for owner types
class OwnerType(str, Enum):
    INDIVIDUAL = "individual"  # Individual owner
    COMPANY = "company"  # Company/Corporate owner
    TRUST = "trust"  # Trust ownership
    JOINT = "joint"  # Joint ownership
    GOVERNMENT = "government"  # Government ownership
    ASSOCIATION = "association"  # Association ownership


# Enumeration for owner statuses
class OwnerStatus(str, Enum):
    ACTIVE = "active"  # Current active owner
    INACTIVE = "inactive"  # Inactive owner
    PENDING = "pending"  # Pending verification
    SUSPENDED = "suspended"  # Temporarily suspended
    BLOCKED = "blocked"  # Blocked owner
    ARCHIVED = "archived"  # Archived owner record


# Model for representing an owner in the building management system
class Owner(TableBase, table=True):
    __tablename__ = "owners"
    # __table_args__ = {'extend_existing': True}

    owner_type: OwnerType = Field(
        sa_column=Column(SQLEnum(OwnerType)),
        default=OwnerType.INDIVIDUAL,
        description="Type of owner"
    )
    status: OwnerStatus = Field(
        sa_column=Column(SQLEnum(OwnerStatus)),
        default=OwnerStatus.ACTIVE,
        description="Status of the owner"
    )
    name: str = Field(..., index=True, description="Name of the owner")
    phone: str = Field(..., description="Primary phone number of the owner")
    alternative_phone: Optional[str] = Field(default=None, description="Alternative phone number")
    emergency_contact_phone: Optional[str] = Field(default=None, description="Emergency contact phone number")
    emergency_contact_name: Optional[str] = Field(default=None, description="Emergency contact name")
    email: Optional[str] = Field(default=None, description="Email address of the owner")
    identification_number: str = Field(..., unique=True, description="Unique identification number")
    whatsapp: Optional[str] = Field(default=None, description="WhatsApp contact")
    telegram: Optional[str] = Field(default=None, description="Telegram contact")
    notes: Optional[str] = Field(default=None, description="Additional notes about the owner")

    # Relationships
    units: List["Unit"] = Relationship(back_populates="owner")
    charges: List["Charge"] = Relationship(back_populates="owner")

    class Config:
        json_schema_extra = {
            "example": {
                "owner_type": "individual",
                "status": "active",
                "name": "John Doe",
                "phone": "+1234567890",
                "alternative_phone": "+0987654321",
                "emergency_contact_phone": "+1122334455",
                "emergency_contact_name": "Jane Doe",
                "email": "john.doe@example.com",
                "identification_number": "ID123456789",
                "whatsapp": "+1234567890",
                "telegram": "@johndoe",
                "notes": "Key holder for building A"
            }
        }


# Forward references for type hints
from app.models.unit import Unit
from app.models.charge import Charge
