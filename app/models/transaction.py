from datetime import datetime
from decimal import Decimal
from typing import Optional
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, Enum as SQLEnum

from app.models.mixins import SoftDeleteMixin, TimestampMixin
# from mixins import TimestampMixin, SoftDeleteMixin
# from app.models.fund import Fund

class TransactionType(str, Enum):
    """Enumeration for transaction types"""
    RENT = "rent"  # Rent payment
    DEPOSIT = "deposit"  # Security deposit
    MAINTENANCE = "maintenance"  # Maintenance fee
    UTILITY = "utility"  # Utility payment
    PARKING = "parking"  # Parking fee
    FINE = "fine"  # Penalties or fines
    REFUND = "refund"  # Refund payment
    ADJUSTMENT = "adjustment"  # Balance adjustment
    OTHER = "other"  # Other transactions


class TransactionStatus(str, Enum):
    """Enumeration for transaction statuses"""
    PENDING = "pending"  # Awaiting processing
    COMPLETED = "completed"  # Successfully processed
    FAILED = "failed"  # Transaction failed
    CANCELLED = "cancelled"  # Transaction cancelled
    REFUNDED = "refunded"  # Transaction refunded
    PARTIAL = "partial"  # Partially paid
    OVERDUE = "overdue"  # Payment overdue
    DISPUTED = "disputed"  # Payment disputed


class PaymentMethod(str, Enum):
    """Enumeration for payment methods"""
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    MOBILE_PAYMENT = "mobile_payment"
    ONLINE_PAYMENT = "online_payment"
    OTHER = "other"


class Transaction(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    __tablename__ = "transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    transaction_type: TransactionType = Field(
        sa_column=Column(SQLEnum(TransactionType)),
    )
    status: TransactionStatus = Field(
        sa_column=Column(SQLEnum(TransactionStatus)),
        default=TransactionStatus.PENDING
    )
    payment_method: PaymentMethod = Field(
        sa_column=Column(SQLEnum(PaymentMethod)),
    )
    building_id: int = Field(foreign_key="buildings.id")
    unit_id: int = Field(foreign_key="units.id")
    tenant_id: int = Field(foreign_key="tenants.id")
    fund_id: int = Field(foreign_key="funds.id")
    type: TransactionType
    amount: float
    description: Optional[str] = None
    reference_number: Optional[str] = None
    due_date: datetime
    payment_date: Optional[datetime] = None
    late_fee: Optional[Decimal] = None
    discount: Optional[Decimal] = None
    notes: Optional[str] = None

    # Relationships
    fund: "Fund" = Relationship(back_populates="transactions")


# Transaction.model_rebuild()