from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field
from app.schemas.mixins import BaseSchema
from app.models.fund import TransactionType, TransactionStatus, PaymentMethod


class TransactionBase(BaseSchema):
    """Base Transaction Schema with common attributes"""
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
    payment_method: PaymentMethod = Field(
        ...,
        description="Method of payment"
    )
    building_id: int = Field(
        ...,
        description="ID of the building"
    )
    unit_id: Optional[int] = Field(
        default=None,
        description="ID of the unit if applicable"
    )
    tenant_id: Optional[int] = Field(
        default=None,
        description="ID of the tenant"
    )
    due_date: datetime = Field(
        ...,
        description="Due date for the payment"
    )
    payment_date: Optional[datetime] = Field(
        default=None,
        description="Date when payment was made"
    )
    reference_number: Optional[str] = Field(
        default=None,
        description="Reference or transaction number",
        max_length=50
    )
    description: str = Field(
        ...,
        description="Transaction description",
        min_length=3,
        max_length=200
    )
    late_fee: Optional[Decimal] = Field(
        default=None,
        description="Late fee amount if applicable",
        ge=0,
        decimal_places=2
    )
    discount: Optional[Decimal] = Field(
        default=None,
        description="Discount amount if applicable",
        ge=0,
        decimal_places=2
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "transaction_type": "rent",
                "amount": "1500.00",
                "status": "completed",
                "payment_method": "bank_transfer",
                "building_id": 1,
                "unit_id": 101,
                "tenant_id": 1,
                "due_date": "2025-01-15 15:24:20",
                "payment_date": "2025-01-15 15:24:20",
                "reference_number": "TRX-2025-001",
                "invoice_number": "INV-2025-001",
                "description": "January 2025 Rent Payment",
                "tags": ["rent", "monthly"]
            }
        }


class TransactionCreate(TransactionBase):
    """Schema for creating a new transaction"""
    pass


class TransactionUpdate(BaseSchema):
    """Schema for updating an existing transaction"""
    status: Optional[TransactionStatus] = None
    payment_method: Optional[PaymentMethod] = None
    payment_date: Optional[datetime] = None
    reference_number: Optional[str] = None
    late_fee: Optional[Decimal] = Field(default=None, ge=0)
    discount: Optional[Decimal] = Field(default=None, ge=0)
    notes: Optional[str] = None


class TransactionInDB(TransactionBase):
    """Schema for transaction as stored in database"""
    id: int = Field(..., description="Unique identifier for the transaction")


class TransactionResponse(TransactionInDB):
    """Schema for transaction response"""
    total_amount: Decimal = Field(
        ...,
        description="Total amount including fees and discounts"
    )
    tenant_name: Optional[str] = Field(
        default=None,
        description="Name of the tenant"
    )
    unit_number: Optional[str] = Field(
        default=None,
        description="Unit number"
    )


class TransactionBulkCreate(BaseSchema):
    """Schema for bulk transaction creation"""
    transactions: List[TransactionCreate] = Field(
        description="List of transactions to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "transactions": [{
                    "transaction_type": "rent",
                    "amount": "1500.00",
                    "status": "completed",
                    "payment_method": "bank_transfer",
                    "building_id": 1,
                    "unit_id": 101,
                    "tenant_id": 1,
                    "due_date": "2025-01-15 15:24:20",
                    "description": "January 2025 Rent Payment",
                    "tags": ["rent", "monthly"]
                }]
            }
        }


class TransactionFilter(BaseSchema):
    """Schema for filtering transactions"""
    building_id: Optional[int] = None
    unit_id: Optional[int] = None
    tenant_id: Optional[int] = None
    transaction_type: Optional[List[TransactionType]] = None
    status: Optional[List[TransactionStatus]] = None
    payment_method: Optional[List[PaymentMethod]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[Decimal] = Field(default=None, gt=0)
    max_amount: Optional[Decimal] = Field(default=None, gt=0)
    is_overdue: Optional[bool] = None
    tags: Optional[List[str]] = None


class TransactionStatistics(BaseSchema):
    """Schema for transaction statistics"""
    total_transactions: int = Field(..., description="Total number of transactions")
    total_amount: Decimal = Field(..., description="Total amount of all transactions")
    pending_amount: Decimal = Field(..., description="Total pending amount")
    overdue_amount: Decimal = Field(..., description="Total overdue amount")
    by_type: dict = Field(..., description="Transactions grouped by type")
    by_status: dict = Field(..., description="Transactions grouped by status")
    by_payment_method: dict = Field(..., description="Transactions grouped by payment method")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_transactions": 500,
                "total_amount": "750000.00",
                "pending_amount": "25000.00",
                "overdue_amount": "5000.00",
                "by_type": {
                    "rent": {"count": 400, "amount": "600000.00"},
                    "utility": {"count": 100, "amount": "150000.00"}
                },
                "by_status": {
                    "completed": {"count": 450, "amount": "720000.00"},
                    "pending": {"count": 50, "amount": "30000.00"}
                },
                "by_payment_method": {
                    "bank_transfer": {"count": 300, "amount": "450000.00"},
                    "credit_card": {"count": 200, "amount": "300000.00"}
                }
            }
        }