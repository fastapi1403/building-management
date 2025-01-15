from datetime import datetime
from decimal import Decimal
from typing import Optional, List

from pydantic import Field

from app.schemas.mixins import BaseSchema
from models.fund import FundType, FundStatus, TransactionType, TransactionStatus, PaymentMethod


class FundBase(BaseSchema):
    """Base Fund Schema with common attributes"""
    name: str = Field(
        ...,
        description="Name of the fund",
        min_length=3,
        max_length=100
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the fund"
    )
    fund_type: FundType = Field(
        ...,
        description="Type of the fund"
    )
    status: FundStatus = Field(
        default=FundStatus.ACTIVE,
        description="Current status of the fund"
    )
    building_id: int = Field(
        ...,
        description="ID of the building this fund belongs to"
    )
    target_amount: Decimal = Field(
        ...,
        description="Target amount for the fund",
        gt=0,
        decimal_places=2
    )
    current_balance: Decimal = Field(
        default=Decimal('0.00'),
        description="Current balance of the fund",
        ge=0,
        decimal_places=2
    )
    minimum_balance: Decimal = Field(
        default=Decimal('0.00'),
        description="Minimum balance to maintain",
        ge=0,
        decimal_places=2
    )
    start_date: datetime = Field(
        ...,
        description="Start date of the fund"
    )
    end_date: Optional[datetime] = Field(
        default=None,
        description="End date of the fund if applicable"
    )
    contribution_frequency: Optional[str] = Field(
        default=None,
        description="Frequency of contributions (monthly, quarterly, yearly)"
    )
    contribution_amount: Optional[Decimal] = Field(
        default=None,
        description="Amount of regular contributions",
        gt=0,
        decimal_places=2
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes about the fund"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorizing the fund"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "name": "Building Maintenance Fund",
                "description": "Fund for regular building maintenance and repairs",
                "fund_type": "maintenance",
                "status": "active",
                "building_id": 1,
                "target_amount": "100000.00",
                "current_balance": "25000.00",
                "minimum_balance": "5000.00",
                "start_date": "2025-01-15 14:46:19",
                "contribution_frequency": "monthly",
                "contribution_amount": "2000.00",
                "tags": ["maintenance", "regular"]
            }
        }


class FundCreate(FundBase):
    """Schema for creating a new fund"""
    pass


class FundUpdate(BaseSchema):
    """Schema for updating an existing fund"""
    name: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    description: Optional[str] = None
    fund_type: Optional[FundType] = None
    status: Optional[FundStatus] = None
    target_amount: Optional[Decimal] = Field(default=None, gt=0)
    current_balance: Optional[Decimal] = Field(default=None, ge=0)
    minimum_balance: Optional[Decimal] = Field(default=None, ge=0)
    end_date: Optional[datetime] = None
    contribution_frequency: Optional[str] = None
    contribution_amount: Optional[Decimal] = Field(default=None, gt=0)
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class FundInDB(FundBase):
    """Schema for fund as stored in database"""
    id: int = Field(..., description="Unique identifier for the fund")


class FundResponse(FundInDB):
    """Schema for fund response"""
    total_contributions: Decimal = Field(
        default=Decimal('0.00'),
        description="Total contributions made to the fund"
    )
    total_withdrawals: Decimal = Field(
        default=Decimal('0.00'),
        description="Total withdrawals made from the fund"
    )
    last_contribution_date: Optional[datetime] = Field(
        default=None,
        description="Date of the last contribution"
    )
    last_withdrawal_date: Optional[datetime] = Field(
        default=None,
        description="Date of the last withdrawal"
    )


class FundBulkCreate(BaseSchema):
    """Schema for bulk fund creation"""
    funds: List[FundCreate] = Field(
        description="List of funds to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "funds": [
                    {
                        "name": "Building Maintenance Fund",
                        "description": "Fund for regular building maintenance",
                        "fund_type": "maintenance",
                        "status": "active",
                        "building_id": 1,
                        "target_amount": "100000.00",
                        "current_balance": "25000.00",
                        "minimum_balance": "5000.00",
                        "start_date": "2025-01-15 14:46:19",
                        "contribution_frequency": "monthly",
                        "contribution_amount": "2000.00",
                        "tags": ["maintenance", "regular"]
                    }
                ]
            }
        }


class FundFilter(BaseSchema):
    """Schema for filtering funds"""
    building_id: Optional[int] = None
    fund_type: Optional[List[FundType]] = None
    status: Optional[List[FundStatus]] = None
    min_balance: Optional[Decimal] = Field(default=None, ge=0)
    max_balance: Optional[Decimal] = Field(default=None, gt=0)
    tags: Optional[List[str]] = None


class FundStatistics(BaseSchema):
    """Schema for fund statistics"""
    total_funds: int = Field(..., description="Total number of funds")
    total_balance: Decimal = Field(..., description="Total balance across all funds")
    total_target: Decimal = Field(..., description="Total target amount across all funds")
    by_type: dict = Field(..., description="Funds grouped by type")
    by_status: dict = Field(..., description="Funds grouped by status")
    funding_ratio: float = Field(..., description="Current total balance / total target")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_funds": 5,
                "total_balance": "150000.00",
                "total_target": "500000.00",
                "by_type": {
                    "maintenance": {"count": 2, "balance": "75000.00", "target": "200000.00"},
                    "reserve": {"count": 3, "balance": "75000.00", "target": "300000.00"}
                },
                "by_status": {
                    "active": {"count": 4, "balance": "140000.00"},
                    "inactive": {"count": 1, "balance": "10000.00"}
                },
                "funding_ratio": 30.0
            }
        }


class FundTransactionBase(BaseSchema):
    """Base Fund Transaction Schema with common attributes"""
    fund_id: int = Field(
        ...,
        description="ID of the fund"
    )
    building_id: int = Field(
        ...,
        description="ID of the building"
    )
    transaction_type: TransactionType = Field(
        ...,
        description="Type of the transaction"
    )
    amount: Decimal = Field(
        ...,
        description="Transaction amount",
        gt=0,
        decimal_places=2
    )
    status: TransactionStatus = Field(
        default=TransactionStatus.PENDING,
        description="Status of the transaction"
    )
    transaction_date: datetime = Field(
        default_factory=lambda: datetime.strptime("2025-01-15 14:52:45", "%Y-%m-%d %H:%M:%S"),
        description="Date and time of the transaction"
    )
    payment_method: PaymentMethod = Field(
        ...,
        description="Method of payment"
    )
    reference_number: Optional[str] = Field(
        default=None,
        description="Reference or transaction number"
    )
    related_fund_id: Optional[int] = Field(
        default=None,
        description="Related fund ID for transfers"
    )
    description: Optional[str] = Field(
        default=None,
        description="Transaction description"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Transaction tags"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "fund_id": 1,
                "building_id": 1,
                "transaction_type": "contribution",
                "amount": "1000.00",
                "status": "completed",
                "transaction_date": "2025-01-15 14:52:45",
                "payment_method": "bank_transfer",
                "reference_number": "TRX-2025-001",
                "description": "Monthly contribution to maintenance fund",
                "tags": ["maintenance", "monthly"]
            }
        }


class FundTransactionCreate(FundTransactionBase):
    """Schema for creating a new fund transaction"""
    pass


class FundTransactionUpdate(BaseSchema):
    """Schema for updating an existing fund transaction"""
    status: Optional[TransactionStatus] = None
    payment_method: Optional[PaymentMethod] = None
    reference_number: Optional[str] = None
    description: Optional[str] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class FundTransactionInDB(FundTransactionBase):
    """Schema for fund transaction as stored in database"""
    id: int = Field(..., description="Unique identifier for the transaction")


class FundTransactionResponse(FundTransactionInDB):
    """Schema for fund transaction response"""
    previous_balance: Decimal = Field(
        ...,
        description="Fund balance before transaction"
    )
    new_balance: Decimal = Field(
        ...,
        description="Fund balance after transaction"
    )
    fund_name: str = Field(
        ...,
        description="Name of the fund"
    )


class FundTransactionBulkCreate(BaseSchema):
    """Schema for bulk fund transaction creation"""
    transactions: List[FundTransactionCreate] = Field(
        description="List of transactions to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "transactions": [
                    {
                        "fund_id": 1,
                        "building_id": 1,
                        "transaction_type": "contribution",
                        "amount": "1000.00",
                        "status": "completed",
                        "transaction_date": "2025-01-15 14:52:45",
                        "payment_method": "bank_transfer",
                        "reference_number": "TRX-2025-001",
                        "description": "Monthly contribution to maintenance fund",
                        "tags": ["maintenance", "monthly"]
                    }
                ]
            }
        }


class FundTransactionFilter(BaseSchema):
    """Schema for filtering fund transactions"""
    fund_id: Optional[int] = None
    building_id: Optional[int] = None
    transaction_type: Optional[List[TransactionType]] = None
    status: Optional[List[TransactionStatus]] = None
    payment_method: Optional[List[PaymentMethod]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[Decimal] = Field(default=None, gt=0)
    max_amount: Optional[Decimal] = Field(default=None, gt=0)
    tags: Optional[List[str]] = None


class FundTransactionStatistics(BaseSchema):
    """Schema for fund transaction statistics"""
    total_transactions: int = Field(..., description="Total number of transactions")
    total_contributions: Decimal = Field(..., description="Total contributions")
    total_withdrawals: Decimal = Field(..., description="Total withdrawals")
    net_balance_change: Decimal = Field(..., description="Net change in balance")
    by_type: dict = Field(..., description="Transactions grouped by type")
    by_status: dict = Field(..., description="Transactions grouped by status")
    by_payment_method: dict = Field(..., description="Transactions grouped by payment method")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_transactions": 100,
                "total_contributions": "50000.00",
                "total_withdrawals": "20000.00",
                "net_balance_change": "30000.00",
                "by_type": {
                    "contribution": {"count": 60, "amount": "50000.00"},
                    "withdrawal": {"count": 40, "amount": "20000.00"}
                },
                "by_status": {
                    "completed": {"count": 95, "amount": "68000.00"},
                    "pending": {"count": 5, "amount": "2000.00"}
                },
                "by_payment_method": {
                    "bank_transfer": {"count": 80, "amount": "60000.00"},
                    "cash": {"count": 20, "amount": "10000.00"}
                }
            }
        }
