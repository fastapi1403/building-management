from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, constr, condecimal
from decimal import Decimal
from enum import Enum


class FundType(str, Enum):
    MAINTENANCE = "maintenance"
    RESERVE = "reserve"
    SINKING = "sinking"
    OPERATING = "operating"
    EMERGENCY = "emergency"
    RENOVATION = "renovation"
    SPECIAL_ASSESSMENT = "special_assessment"


class FundStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    FROZEN = "frozen"
    DEPLETED = "depleted"
    PENDING_APPROVAL = "pending_approval"


class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    TRANSFER = "transfer"
    INTEREST = "interest"
    ADJUSTMENT = "adjustment"


# Base Schema
class FundBase(BaseModel):
    name: constr(min_length=3, max_length=100)
    description: constr(max_length=500)
    fund_type: FundType
    status: FundStatus = FundStatus.ACTIVE
    currency: constr(max_length=3) = "INR"

    building_id: int
    minimum_balance: condecimal(ge=0, max_digits=12, decimal_places=2) = Decimal("0.00")
    target_amount: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]

    requires_approval: bool = True
    approval_threshold: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]
    withdrawal_limit: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]

    tags: List[str] = []

    @validator('approval_threshold')
    def validate_approval_threshold(cls, v, values):
        if values.get('requires_approval') and not v:
            raise ValueError("Approval threshold is required when approval is required")
        return v


# Create Schema
class FundCreate(FundBase):
    manager: str = Field(default="fastapi1403")
    notes: Optional[str] = None
    current_balance: condecimal(ge=0, max_digits=12, decimal_places=2) = Decimal("0.00")


# Update Schema
class FundUpdate(BaseModel):
    name: Optional[constr(min_length=3, max_length=100)]
    description: Optional[constr(max_length=500)]
    status: Optional[FundStatus]
    target_amount: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]
    minimum_balance: Optional[condecimal(ge=0, max_digits=12, decimal_places=2)]
    withdrawal_limit: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]
    requires_approval: Optional[bool]
    approval_threshold: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]
    notes: Optional[str]
    tags: Optional[List[str]]


# Transaction Schema
class FundTransaction(BaseModel):
    transaction_type: TransactionType
    amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    reference_number: constr(max_length=50)
    description: constr(max_length=500)
    initiated_by: str = Field(default="fastapi1403")
    notes: Optional[str]

    cost_id: Optional[int]
    charge_id: Optional[int]

    @validator('amount')
    def validate_amount(cls, v, values):
        if values.get('transaction_type') in [TransactionType.WITHDRAWAL, TransactionType.TRANSFER]:
            if v <= 0:
                raise ValueError("Withdrawal amount must be greater than zero")
        return v


# DB Schema
class FundInDB(FundBase):
    id: int
    current_balance: condecimal(max_digits=12, decimal_places=2)
    manager: str
    last_audit_date: Optional[datetime]
    next_audit_date: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Response Schemas
class FundResponse(FundInDB):
    available_balance: condecimal(max_digits=12, decimal_places=2)
    is_low_balance: bool
    balance_percentage: float
    days_to_next_audit: Optional[int]

    @validator('available_balance', pre=True)
    def calculate_available_balance(cls, v, values):
        current = values.get('current_balance', Decimal("0.00"))
        minimum = values.get('minimum_balance', Decimal("0.00"))
        return max(Decimal("0.00"), current - minimum)

    @validator('is_low_balance', pre=True)
    def calculate_low_balance(cls, v, values):
        current = values.get('current_balance', Decimal("0.00"))
        minimum = values.get('minimum_balance', Decimal("0.00"))
        threshold = minimum * Decimal("1.1")  # 10% above minimum
        return current <= threshold

    @validator('balance_percentage', pre=True)
    def calculate_balance_percentage(cls, v, values):
        target = values.get('target_amount')
        current = values.get('current_balance', Decimal("0.00"))
        if not target or target == 0:
            return 100.0
        return float(current / target * 100)

    @validator('days_to_next_audit', pre=True)
    def calculate_days_to_audit(cls, v, values):
        next_audit = values.get('next_audit_date')
        if not next_audit:
            return None
        return (next_audit.date() - date.today()).days


class FundList(BaseModel):
    funds: List[FundResponse]
    total_count: int
    total_balance: condecimal(max_digits=14, decimal_places=2)
    total_available: condecimal(max_digits=14, decimal_places=2)
    total_minimum: condecimal(max_digits=14, decimal_places=2)


# Approval Schema
class FundApprovalRequest(BaseModel):
    requested_amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    purpose: constr(max_length=500)
    justification: constr(max_length=1000)
    requested_by: str = Field(default="fastapi1403")
    supporting_documents: List[str] = []
    notes: Optional[str]


# Statistics Schema
class FundStatistics(BaseModel):
    total_funds: int
    total_balance: condecimal(max_digits=14, decimal_places=2)
    total_available: condecimal(max_digits=14, decimal_places=2)
    total_minimum: condecimal(max_digits=14, decimal_places=2)
    funds_by_type: Dict[FundType, Dict[str, Any]]
    monthly_transactions: List[Dict[str, Any]]
    approval_statistics: Dict[str, Any]
    balance_trends: List[Dict[str, Any]]

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v),
            datetime: lambda v: v.isoformat()
        }


# Filter Schema
class FundFilter(BaseModel):
    fund_type: Optional[List[FundType]]
    status: Optional[List[FundStatus]]
    min_balance: Optional[condecimal(ge=0)]
    max_balance: Optional[condecimal(ge=0)]
    is_low_balance: Optional[bool]
    requires_approval: Optional[bool]
    tags: Optional[List[str]]