from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, constr, condecimal
from decimal import Decimal
from enum import Enum


class TransactionStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REVERSED = "reversed"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"
    DISPUTED = "disputed"


class TransactionType(str, Enum):
    PAYMENT = "payment"
    REFUND = "refund"
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    ADJUSTMENT = "adjustment"
    FEE = "fee"
    INTEREST = "interest"


class PaymentMethod(str, Enum):
    CASH = "cash"
    BANK_TRANSFER = "bank_transfer"
    CHEQUE = "cheque"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    UPI = "upi"
    ONLINE = "online"
    OTHER = "other"


# Base Schema
class TransactionBase(BaseModel):
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    currency: constr(max_length=3) = "INR"
    type: TransactionType
    payment_method: PaymentMethod
    description: constr(max_length=500)

    building_id: int
    unit_id: Optional[int]
    owner_id: Optional[int]
    tenant_id: Optional[int]
    charge_id: Optional[int]
    cost_id: Optional[int]
    fund_id: Optional[int]

    payment_reference: Optional[constr(max_length=100)]
    bank_reference: Optional[constr(max_length=100)]
    cheque_number: Optional[constr(max_length=50)]

    tags: List[str] = []


# Create Schema
class TransactionCreate(TransactionBase):
    transaction_number: Optional[str] = None  # Will be generated if not provided
    status: TransactionStatus = TransactionStatus.PENDING
    payment_date: datetime = Field(default_factory=lambda: datetime.now())
    processed_by: str = Field(default="fastapi1403")
    notes: Optional[str]

    gateway_name: Optional[str]
    gateway_transaction_id: Optional[str]
    gateway_response: Optional[Dict[str, Any]]

    @validator('payment_date')
    def validate_payment_date(cls, v):
        if v > datetime.now():
            raise ValueError("Payment date cannot be in the future")
        return v


# Update Schema
class TransactionUpdate(BaseModel):
    status: Optional[TransactionStatus]
    payment_reference: Optional[str]
    bank_reference: Optional[str]
    gateway_response: Optional[Dict[str, Any]]
    notes: Optional[str]
    approved_by: Optional[str]
    approved_at: Optional[datetime]


# DB Schema
class TransactionInDB(TransactionBase):
    id: int
    transaction_number: str
    status: TransactionStatus
    payment_date: datetime
    processed_by: str
    approved_by: Optional[str]
    approved_at: Optional[datetime]

    gateway_name: Optional[str]
    gateway_transaction_id: Optional[str]
    gateway_response: Optional[Dict[str, Any]]

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Response Schema
class TransactionResponse(TransactionInDB):
    processing_time: Optional[int]  # in seconds
    days_since_transaction: int
    settlement_status: str
    related_entity_type: str
    related_entity_id: int

    @validator('processing_time', pre=True)
    def calculate_processing_time(cls, v, values):
        created = values.get('created_at')
        approved = values.get('approved_at')
        if not approved or not created:
            return None
        return int((approved - created).total_seconds())

    @validator('days_since_transaction', pre=True)
    def calculate_days_since(cls, v, values):
        payment_date = values.get('payment_date')
        return (datetime.now() - payment_date).days

    @validator('settlement_status', pre=True)
    def determine_settlement_status(cls, v, values):
        status = values.get('status')
        if status == TransactionStatus.COMPLETED:
            return "Settled"
        elif status in [TransactionStatus.FAILED, TransactionStatus.CANCELLED]:
            return "Failed"
        return "Pending Settlement"

    @validator('related_entity_type', 'related_entity_id', pre=True)
    def determine_related_entity(cls, v, values):
        if values.get('charge_id'):
            return ("charge", values['charge_id'])
        elif values.get('cost_id'):
            return ("cost", values['cost_id'])
        elif values.get('fund_id'):
            return ("fund", values['fund_id'])
        return ("building", values['building_id'])


# Split Schema
class TransactionSplit(BaseModel):
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    category: str
    description: str
    fund_id: Optional[int]

    @validator('amount')
    def validate_split_amount(cls, v, values):
        if v <= 0:
            raise ValueError("Split amount must be greater than zero")
        return v


# Attachment Schema
class TransactionAttachment(BaseModel):
    file_name: constr(max_length=255)
    file_type: constr(max_length=50)
    file_size: int
    file_path: str
    uploaded_by: str = Field(default="fastapi1403")
    description: Optional[str]


# Filter Schema
class TransactionFilter(BaseModel):
    status: Optional[List[TransactionStatus]]
    type: Optional[List[TransactionType]]
    payment_method: Optional[List[PaymentMethod]]
    date_from: Optional[date]
    date_to: Optional[date]
    min_amount: Optional[condecimal(ge=0)]
    max_amount: Optional[condecimal(ge=0)]
    entity_type: Optional[str]
    entity_id: Optional[int]
    tags: Optional[List[str]]


# Statistics Schema
class TransactionStatistics(BaseModel):
    total_transactions: int
    total_amount: condecimal(max_digits=14, decimal_places=2)
    successful_transactions: int
    failed_transactions: int
    average_processing_time: float
    transactions_by_type: Dict[TransactionType, Dict[str, Any]]
    transactions_by_payment_method: Dict[PaymentMethod, Dict[str, Any]]
    daily_totals: List[Dict[str, Any]]
    success_rate: float

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }


# Reconciliation Schema
class TransactionReconciliation(BaseModel):
    transaction_id: int
    reconciled: bool
    reconciliation_date: datetime = Field(default_factory=lambda: datetime.now())
    reconciled_by: str = Field(default="fastapi1403")
    notes: Optional[str]
    differences: List[Dict[str, Any]] = []