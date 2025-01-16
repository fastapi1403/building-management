from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional

from sqlalchemy import Column, Enum as SQLEnum
from sqlmodel import Field, Relationship

from app.models.base import TableBase


# Enumeration for transaction types
class TransactionType(str, Enum):
    RENT = "rent"  # Rent payment
    DEPOSIT = "deposit"  # Security deposit
    MAINTENANCE = "maintenance"  # Maintenance fee
    UTILITY = "utility"  # Utility payment
    PARKING = "parking"  # Parking fee
    FINE = "fine"  # Penalties or fines
    REFUND = "refund"  # Refund payment
    ADJUSTMENT = "adjustment"  # Balance adjustment
    OTHER = "other"  # Other transactions


# Enumeration for transaction statuses
class TransactionStatus(str, Enum):
    PENDING = "pending"  # Awaiting processing
    COMPLETED = "completed"  # Successfully processed
    FAILED = "failed"  # Transaction failed
    CANCELLED = "cancelled"  # Transaction cancelled
    REFUNDED = "refunded"  # Transaction refunded
    PARTIAL = "partial"  # Partially paid
    OVERDUE = "overdue"  # Payment overdue
    DISPUTED = "disputed"  # Payment disputed


# Enumeration for payment methods
class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    MOBILE_PAYMENT = "mobile_payment"
    ONLINE_PAYMENT = "online_payment"
    OTHER = "other"


# Model for representing a transaction in the building management system
class Transaction(TableBase, table=True):
    __tablename__ = "transactions"
    __table_args__ = {'extend_existing': True}

    transaction_type: TransactionType = Field(
        sa_column=Column(SQLEnum(TransactionType)),
        description="Type of the transaction"
    )
    status: TransactionStatus = Field(
        sa_column=Column(SQLEnum(TransactionStatus)),
        default=TransactionStatus.PENDING,
        description="Status of the transaction"
    )
    payment_method: PaymentMethod = Field(
        sa_column=Column(SQLEnum(PaymentMethod)),
        description="Payment method used for the transaction"
    )
    building_id: int = Field(foreign_key="buildings.id", description="ID of the associated building")
    unit_id: int = Field(foreign_key="units.id", description="ID of the associated unit")
    tenant_id: int = Field(foreign_key="tenants.id", description="ID of the associated tenant")
    fund_id: int = Field(foreign_key="funds.id", description="ID of the associated fund")
    type: TransactionType = Field(description="Type of the transaction")
    amount: float = Field(description="Amount of the transaction")
    description: Optional[str] = Field(default=None, description="Description of the transaction")
    reference_number: Optional[str] = Field(default=None, description="Reference number for the transaction")
    due_date: datetime = Field(description="Due date for the transaction")
    payment_date: Optional[datetime] = Field(default=None, description="Payment date of the transaction")
    late_fee: Optional[Decimal] = Field(default=None, description="Late fee applied to the transaction")
    discount: Optional[Decimal] = Field(default=None, description="Discount applied to the transaction")
    notes: Optional[str] = Field(default=None, description="Additional notes about the transaction")

    # Relationships
    fund: "Fund" = Relationship(back_populates="transactions")

    class Config:
        json_schema_extra = {
            "example": {
                "transaction_type": "rent",
                "status": "pending",
                "payment_method": "bank_transfer",
                "building_id": 1,
                "unit_id": 101,
                "tenant_id": 1001,
                "fund_id": 201,
                "type": "rent",
                "amount": 1500.00,
                "description": "Monthly rent for January",
                "reference_number": "TXN1234567890",
                "due_date": "2025-01-01T00:00:00",
                "payment_date": None,
                "late_fee": None,
                "discount": None,
                "notes": "Payment to be made via bank transfer"
            }
        }


# Forward references for type hints
from app.models.fund import Fund
