from datetime import datetime, UTC
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Enum as SQLEnum, Index
from decimal import Decimal

from base import TimestampMixin
from building import Building
from cost import Cost
from charge import Charge


class FundType(str, Enum):
    """Enum for fund types"""
    MAINTENANCE = "maintenance"
    RESERVE = "reserve"
    SINKING = "sinking"
    OPERATING = "operating"
    EMERGENCY = "emergency"
    RENOVATION = "renovation"
    SPECIAL_ASSESSMENT = "special_assessment"


class FundStatus(str, Enum):
    """Enum for fund status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    FROZEN = "frozen"
    DEPLETED = "depleted"
    PENDING_APPROVAL = "pending_approval"


class TransactionType(str, Enum):
    """Enum for fund transactions"""
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    INTEREST = "interest"
    ADJUSTMENT = "adjustment"


class Fund(TimestampMixin, table=True):
    """
    Model for managing building funds and their transactions
    """
    __tablename__ = "funds"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Fund Information
    name: str = Field(..., max_length=100)
    description: str = Field(..., max_length=500)
    fund_type: FundType = Field(
        sa_column=Column(SQLEnum(FundType)),
        default=FundType.MAINTENANCE
    )
    status: FundStatus = Field(
        sa_column=Column(SQLEnum(FundStatus)),
        default=FundStatus.ACTIVE
    )

    # Financial Details
    current_balance: Decimal = Field(default=Decimal('0.00'))
    target_amount: Optional[Decimal] = Field(default=None)
    minimum_balance: Decimal = Field(default=Decimal('0.00'))
    currency: str = Field(default="INR", max_length=3)

    # Association
    building_id: int = Field(..., foreign_key="buildings.id")

    # Fund Management
    manager: str = Field(default="fastapi1403", max_length=100)
    last_audit_date: Optional[datetime] = Field(default=None)
    next_audit_date: Optional[datetime] = Field(default=None)

    # Rules and Restrictions
    withdrawal_limit: Optional[Decimal] = Field(default=None)
    requires_approval: bool = Field(default=True)
    approval_threshold: Optional[Decimal] = Field(default=None)

    # Metadata
    notes: Optional[str] = Field(default=None, max_length=1000)
    tags: List[str] = Field(default_factory=list)

    # Relationships
    building: "Building" = Relationship(back_populates="funds")
    transactions: List["FundTransaction"] = Relationship(back_populates="fund")
    approvals: List["FundApproval"] = Relationship(back_populates="fund")

    __table_args__ = (
        Index('ix_funds_building_type', 'building_id', 'fund_type'),
        Index('ix_funds_status', 'status'),
    )

    class Config:
        arbitrary_types_allowed = True

    @property
    def available_balance(self) -> Decimal:
        """Calculate available balance considering minimum balance"""
        return max(Decimal('0.00'), self.current_balance - self.minimum_balance)

    @property
    def is_low_balance(self) -> bool:
        """Check if fund is near minimum balance"""
        threshold = self.minimum_balance * Decimal('1.1')  # 10% above minimum
        return self.current_balance <= threshold


class FundTransaction(TimestampMixin, table=True):
    """
    Model for tracking fund transactions
    """
    __tablename__ = "fund_transactions"

    id: Optional[int] = Field(default=None, primary_key=True)
    fund_id: int = Field(..., foreign_key="funds.id")

    # Transaction Details
    transaction_type: TransactionType = Field(
        sa_column=Column(SQLEnum(TransactionType))
    )
    amount: Decimal = Field(...)
    balance_after: Decimal = Field(...)
    reference_number: str = Field(..., max_length=50)

    # Related Information
    cost_id: Optional[int] = Field(default=None, foreign_key="costs.id")
    charge_id: Optional[int] = Field(default=None, foreign_key="charges.id")

    # Transaction Metadata
    description: str = Field(..., max_length=500)
    initiated_by: str = Field(default="fastapi1403", max_length=100)
    approved_by: Optional[str] = Field(default=None, max_length=100)
    transaction_date: datetime = Field(default_factory=lambda: datetime.now(UTC))
    notes: Optional[str] = Field(default=None, max_length=1000)

    # Relationships
    fund: Fund = Relationship(back_populates="transactions")
    cost: Optional["Cost"] = Relationship(back_populates="fund_transactions")
    charge: Optional["Charge"] = Relationship(back_populates="fund_transactions")

    __table_args__ = (
        Index('ix_fund_transactions_date', 'transaction_date'),
        Index('ix_fund_transactions_type', 'transaction_type'),
    )


class FundApproval(TimestampMixin, table=True):
    """
    Model for managing fund transaction approvals
    """
    __tablename__ = "fund_approvals"

    id: Optional[int] = Field(default=None, primary_key=True)
    fund_id: int = Field(..., foreign_key="funds.id")
    transaction_id: Optional[int] = Field(default=None, foreign_key="fund_transactions.id")

    # Approval Details
    requested_amount: Decimal = Field(...)
    purpose: str = Field(..., max_length=500)
    requested_by: str = Field(default="fastapi1403", max_length=100)
    approved_by: Optional[str] = Field(default=None, max_length=100)
    approved_date: Optional[datetime] = Field(default=None)
    status: str = Field(default="pending")

    # Supporting Information
    justification: str = Field(..., max_length=1000)
    supporting_documents: List[str] = Field(default_factory=list)
    notes: Optional[str] = Field(default=None, max_length=1000)

    # Relationships
    fund: Fund = Relationship(back_populates="approvals")
    transaction: Optional[FundTransaction] = Relationship(back_populates="approval")


# Type annotations for relationships
Fund.model_rebuild()
FundTransaction.model_rebuild()
FundApproval.model_rebuild()