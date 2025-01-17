from datetime import datetime, UTC
from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, Relationship

from app.models.base import TableBase


# Enum for charge status
class ChargeStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    PARTIALLY_PAID = "partially_paid"
    DISPUTED = "disputed"


# Enum for charge types
class ChargeType(str, Enum):
    RECURRING = "recurring"
    MAINTENANCE = "maintenance"
    UTILITY = "utility"
    PARKING = "parking"
    RENOVATION = "renovation"
    PENALTY = "penalty"
    DEPOSIT = "deposit"
    RENT = "rent"
    OTHER = "other"


# Enum for recurring charge frequency
class ChargeFrequency(str, Enum):
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


# Model for managing charges/fees in the building management system
class Charge(TableBase, table=True):
    __tablename__ = "charges"
    # __table_args__ = {'extend_existing': True}

    # Charge details
    title: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    amount: float = Field(..., gt=0)

    # Charge classification
    type: ChargeType = Field(
        sa_column=Column(SQLEnum(ChargeType)),
        default=ChargeType.MAINTENANCE
    )
    status: ChargeStatus = Field(
        sa_column=Column(SQLEnum(ChargeStatus)),
        default=ChargeStatus.PENDING
    )

    # Charge schedule
    due_date: datetime = Field(...)
    frequency: ChargeFrequency = Field(
        sa_column=Column(SQLEnum(ChargeFrequency)),
        default=ChargeFrequency.ONCE
    )
    recurring: bool = Field(default=False)

    # Payment tracking
    amount_paid: float = Field(default=0.0)
    last_payment_date: Optional[datetime] = Field(default=None)
    payment_reference: Optional[str] = Field(default=None, max_length=100)

    # Related entities
    unit_id: Optional[int] = Field(default=None, foreign_key="units.id")
    owner_id: Optional[int] = Field(default=None, foreign_key="owners.id")
    tenant_id: Optional[int] = Field(default=None, foreign_key="tenants.id")
    building_id: int = Field(..., foreign_key="buildings.id")

    # Metadata
    generated_by: str = Field(..., max_length=100)  # User or system that generated the charge
    notes: Optional[str] = Field(default=None, max_length=1000)
    tax_rate: Optional[float] = Field(default=0.0)
    is_taxable: bool = Field(default=False)

    # Relationships
    unit: Optional["Unit"] = Relationship(back_populates="charges")
    owner: Optional["Owner"] = Relationship(back_populates="charges")
    tenant: Optional["Tenant"] = Relationship(back_populates="charges")
    building: "Building" = Relationship(back_populates="charges")
    payments: List["Payment"] = Relationship(back_populates="charge")
    fund_transactions: List["FundTransaction"] = Relationship(back_populates="charge")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Monthly Maintenance Fee",
                "description": "Monthly maintenance fee for January",
                "amount": 100.0,
                "type": "maintenance",
                "status": "pending",
                "due_date": "2025-01-01T00:00:00Z",
                "frequency": "monthly",
                "recurring": True,
                "amount_paid": 0.0,
                "generated_by": "admin",
                "tax_rate": 5.0,
                "is_taxable": True
            }
        }

    @property
    def tax_amount(self) -> float:
        """Calculate tax amount if charge is taxable"""
        if self.is_taxable and self.tax_rate > 0:
            return round(self.amount * (self.tax_rate / 100), 2)
        return 0.0

    @property
    def total_amount(self) -> float:
        """Calculate total amount including tax"""
        return round(self.amount + self.tax_amount, 2)

    @property
    def balance_due(self) -> float:
        """Calculate remaining balance"""
        return round(self.total_amount - self.amount_paid, 2)

    @property
    def is_overdue(self) -> bool:
        """Check if charge is overdue"""
        return (
                self.status != ChargeStatus.PAID and
                self.due_date < datetime.now(UTC) and
                self.balance_due > 0
        )

    def update_status(self) -> None:
        """Update charge status based on payments"""
        if self.balance_due <= 0:
            self.status = ChargeStatus.PAID
        elif self.amount_paid > 0:
            self.status = ChargeStatus.PARTIALLY_PAID
        elif self.is_overdue:
            self.status = ChargeStatus.OVERDUE


# Model for tracking payments against charges
class Payment(TableBase, table=True):
    __tablename__ = "payments"
    # __table_args__ = {'extend_existing': True}

    charge_id: int = Field(..., foreign_key="charges.id")
    amount: float = Field(..., gt=0)
    payment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=100)
    notes: Optional[str] = Field(default=None, max_length=500)

    # Relationship
    charge: Charge = Relationship(back_populates="payments")

    class Config:
        json_schema_extra = {
            "example": {
                "charge_id": 1,
                "amount": 50.0,
                "payment_date": "2025-01-15T00:00:00Z",
                "payment_method": "credit_card",
                "transaction_id": "abc123",
                "notes": "Payment for January maintenance fee"
            }
        }


# Import at the bottom to avoid circular imports
from app.models.building import Building  # noqa: E402
from app.models.owner import Owner  # noqa: E402
from app.models.tenant import Tenant  # noqa: E402
from app.models.unit import Unit  # noqa: E402
from app.models.fund import FundTransaction  # noqa: E402