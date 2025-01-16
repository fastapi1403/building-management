from datetime import datetime, UTC
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Enum as SQLEnum

from app.db import TableBase


# from mixins import TimestampMixin, SoftDeleteMixin
# from .unit import Unit
# from .owner import Owner
# from .tenant import Tenant
# from .building import Building


class ChargeStatus(str, Enum):
    """Enum for charge status"""
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    PARTIALLY_PAID = "partially_paid"
    DISPUTED = "disputed"


class ChargeType(str, Enum):
    """Enum for charge types"""
    RECURRING = "recurring"
    MAINTENANCE = "maintenance"
    UTILITY = "utility"
    PARKING = "parking"
    RENOVATION = "renovation"
    PENALTY = "penalty"
    DEPOSIT = "deposit"
    RENT = "rent"
    OTHER = "other"


class ChargeFrequency(str, Enum):
    """Enum for recurring charge frequency"""
    ONCE = "once"
    DAILY = "daily"
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


class Charge(TableBase, table=True):
    """
    Model for managing charges/fees in the building management system
    """
    __tablename__ = "charges"

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
    payments: list["Payment"] = Relationship(back_populates="charge")

    class Config:
        arbitrary_types_allowed = True

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


class Payment(TableBase, table=True):
    """
    Model for tracking payments against charges
    """
    __tablename__ = "payments"

    charge_id: int = Field(..., foreign_key="charges.id")
    amount: float = Field(..., gt=0)
    payment_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    payment_method: str = Field(..., max_length=50)
    transaction_id: str = Field(..., max_length=100)
    notes: Optional[str] = Field(default=None, max_length=500)

    # Relationship
    charge: Charge = Relationship(back_populates="payments")

    class Config:
        arbitrary_types_allowed = True


# Forward references for type hints
from app.models.owner import Owner
from app.models.tenant import Tenant
from app.models.building import Building
from app.models.unit import Unit
