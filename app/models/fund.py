from datetime import datetime, UTC
from decimal import Decimal
from enum import Enum
from typing import Optional, List

from sqlalchemy import Column, Enum as SQLEnum, Index
from sqlmodel import Field, Relationship

from app.models.base import TableBase


# Enum for fund types
class FundType(str, Enum):
    MAINTENANCE = "maintenance"  # Regular maintenance fund
    RESERVE = "reserve"  # Reserve/emergency fund
    OPERATIONAL = "operational"  # Day-to-day operations
    RENOVATION = "renovation"  # Renovation projects
    SPECIAL_PROJECT = "special_project"  # Special building projects
    EMERGENCY = "emergency"  # Emergency situations
    SINKING = "sinking"  # Long-term capital expenses
    OTHER = "other"  # Other fund types


# Enum for fund status
class FundStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    DEPLETED = "depleted"
    FROZEN = "frozen"
    PENDING_APPROVAL = "pending_approval"
    CLOSED = "closed"


# Enumeration for transaction types
class TransactionType(str, Enum):
    CONTRIBUTION = "contribution"  # Money added to fund
    WITHDRAWAL = "withdrawal"  # Money taken from fund
    TRANSFER_IN = "transfer_in"  # Transfer from another fund
    TRANSFER_OUT = "transfer_out"  # Transfer to another fund
    INTEREST = "interest"  # Interest earned
    ADJUSTMENT = "adjustment"  # Balance adjustment
    REFUND = "refund"  # Refund to fund
    FEE = "fee"  # Bank or service fees


# Enumeration for transaction statuses
class TransactionStatus(str, Enum):
    PENDING = "pending"  # Awaiting processing
    COMPLETED = "completed"  # Successfully processed
    FAILED = "failed"  # Transaction failed
    CANCELLED = "cancelled"  # Transaction cancelled
    REVERSED = "reversed"  # Transaction reversed
    PROCESSING = "processing"  # Currently processing


# Enumeration for payment methods
class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    ONLINE_PAYMENT = "online_payment"
    INTERNAL_TRANSFER = "internal_transfer"
    OTHER = "other"


# Model for managing building funds and their transactions
class Fund(TableBase, table=True):
    __tablename__ = "funds"
    # __table_args__ = {'extend_existing': True}

    # Fund Information
    name: str = Field(..., max_length=100, description="Name of the fund")
    description: str = Field(..., max_length=500, description="Description of the fund")
    fund_type: FundType = Field(
        sa_column=Column(SQLEnum(FundType)),
        default=FundType.MAINTENANCE,
        description="Type of the fund"
    )
    status: FundStatus = Field(
        sa_column=Column(SQLEnum(FundStatus)),
        default=FundStatus.ACTIVE,
        description="Status of the fund"
    )

    # Financial Details
    current_balance: Decimal = Field(default=Decimal('0.00'), description="Current balance of the fund")
    target_amount: Optional[Decimal] = Field(default=None, description="Target amount for the fund")
    minimum_balance: Decimal = Field(default=Decimal('0.00'), description="Minimum required balance for the fund")

    # Association
    building_id: int = Field(..., foreign_key="buildings.id", description="ID of the building this fund belongs to")

    # Fund Management
    manager: str = Field(default="fastapi1403", max_length=100, description="Manager of the fund")
    last_audit_date: Optional[datetime] = Field(default=None, description="Date of the last audit")
    next_audit_date: Optional[datetime] = Field(default=None, description="Date of the next scheduled audit")

    # Rules and Restrictions
    withdrawal_limit: Optional[Decimal] = Field(default=None, description="Maximum withdrawal limit")
    requires_approval: bool = Field(default=True, description="Whether withdrawals require approval")
    approval_threshold: Optional[Decimal] = Field(default=None,
                                                  description="Threshold above which approval is required")

    # Metadata
    notes: Optional[str] = Field(default=None, max_length=1000, description="Additional notes about the fund")

    # Relationships
    building: "Building" = Relationship(back_populates="funds")
    transactions: List["Transaction"] = Relationship(back_populates="fund")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Maintenance Fund",
                "description": "Fund for regular maintenance expenses",
                "fund_type": "maintenance",
                "status": "active",
                "current_balance": "10000.00",
                "target_amount": "20000.00",
                "minimum_balance": "1000.00",
                "building_id": 1,
                "manager": "fastapi1403",
                "requires_approval": True
            }
        }

    @property
    def available_balance(self) -> Decimal:
        """Calculate available balance considering minimum balance"""
        return max(Decimal('0.00'), self.current_balance - self.minimum_balance)

    @property
    def is_low_balance(self) -> bool:
        """Check if fund is near minimum balance"""
        threshold = self.minimum_balance * Decimal('1.1')  # 10% above minimum
        return self.current_balance <= threshold


# Model for tracking fund transactions
class FundTransaction(TableBase, table=True):
    __tablename__ = "fund_transactions"
    # __table_args__ = {'extend_existing': True}

    fund_id: int = Field(..., foreign_key="funds.id", description="ID of the associated fund")
    status: TransactionStatus = Field(
        sa_column=Column(SQLEnum(TransactionStatus)),
        default=TransactionStatus.PENDING,
        description="Status of the transaction"
    )
    payment_method: PaymentMethod = Field(
        sa_column=Column(SQLEnum(PaymentMethod)),
        default=PaymentMethod.BANK_TRANSFER,
        description="Method used for the transaction"
    )

    # Transaction Details
    transaction_type: TransactionType = Field(
        sa_column=Column(SQLEnum(TransactionType)),
        description="Type of the transaction"
    )
    amount: Decimal = Field(..., description="Amount of the transaction")
    balance_after: Decimal = Field(..., description="Balance after the transaction")
    reference_number: str = Field(..., max_length=50, description="Reference number for the transaction")

    # Related Information
    cost_id: Optional[int] = Field(default=None, foreign_key="costs.id",
                                   description="ID of the associated cost, if any")
    charge_id: Optional[int] = Field(default=None, foreign_key="charges.id",
                                     description="ID of the associated charge, if any")

    # Transaction Metadata
    description: str = Field(..., max_length=500, description="Description of the transaction")
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Date of the transaction")
    notes: Optional[str] = Field(default=None, max_length=1000, description="Additional notes about the transaction")

    # Relationships
    fund: Fund = Relationship(back_populates="transactions")
    cost: Optional["Cost"] = Relationship(back_populates="fund_transactions")
    charge: Optional["Charge"] = Relationship(back_populates="fund_transactions")
    transactions: List["FundTransaction"] = Relationship(back_populates="fund")

    class Config:
        json_schema_extra = {
            "example": {
                "fund_id": 1,
                "status": "pending",
                "payment_method": "bank_transfer",
                "transaction_type": "contribution",
                "amount": "500.00",
                "balance_after": "10500.00",
                "reference_number": "TXN12345",
                "description": "Contribution to the maintenance fund",
                "transaction_date": "2025-01-16T17:06:02Z"
            }
        }


# Forward references for type hints
from app.models.building import Building
from app.models.charge import Charge
from app.models.cost import Cost
from app.models.transaction import Transaction
