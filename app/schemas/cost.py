from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator, constr, condecimal
from decimal import Decimal
from enum import Enum


class CostCategory(str, Enum):
    MAINTENANCE = "maintenance"
    REPAIR = "repair"
    UTILITY = "utility"
    STAFF = "staff"
    SECURITY = "security"
    CLEANING = "cleaning"
    RENOVATION = "renovation"
    INSURANCE = "insurance"
    TAXES = "taxes"
    EQUIPMENT = "equipment"
    SUPPLIES = "supplies"
    EMERGENCY = "emergency"
    OTHER = "other"


class CostPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CostStatus(str, Enum):
    PLANNED = "planned"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


# Base Schema
class CostBase(BaseModel):
    title: constr(min_length=3, max_length=200)
    description: constr(max_length=1000)
    category: CostCategory
    priority: CostPriority = CostPriority.MEDIUM
    status: CostStatus = CostStatus.PLANNED

    estimated_amount: condecimal(gt=0, max_digits=12, decimal_places=2)
    currency: constr(max_length=3) = "INR"
    planned_date: date

    building_id: int
    unit_id: Optional[int] = None
    floor_id: Optional[int] = None
    vendor_id: Optional[int] = None

    is_recurring: bool = False
    frequency_months: Optional[int] = None
    budget_code: Optional[constr(max_length=50)] = None
    tags: List[str] = []

    @validator('planned_date')
    def validate_planned_date(cls, v):
        if v < date.today():
            raise ValueError("Planned date cannot be in the past")
        return v

    @validator('frequency_months')
    def validate_frequency_months(cls, v, values):
        if values.get('is_recurring') and not v:
            raise ValueError("Frequency months is required for recurring costs")
        if v is not None and (v < 1 or v > 60):
            raise ValueError("Frequency months must be between 1 and 60")
        return v


# Create Schema
class CostCreate(CostBase):
    created_by: str = Field(default="fastapi1403")
    notes: Optional[str] = None
    warranty_expires: Optional[date] = None
    purchase_order: Optional[constr(max_length=50)] = None


# Update Schema
class CostUpdate(BaseModel):
    title: Optional[constr(min_length=3, max_length=200)]
    description: Optional[constr(max_length=1000)]
    status: Optional[CostStatus]
    priority: Optional[CostPriority]
    actual_amount: Optional[condecimal(gt=0, max_digits=12, decimal_places=2)]
    completion_date: Optional[datetime]
    notes: Optional[str]
    tags: Optional[List[str]]

    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }


# DB Schema
class CostInDB(CostBase):
    id: int
    actual_amount: Optional[condecimal(max_digits=12, decimal_places=2)]
    actual_date: Optional[datetime]
    completion_date: Optional[datetime]
    variance_amount: Optional[condecimal(max_digits=12, decimal_places=2)]

    created_by: str
    approved_by: Optional[str]
    approved_date: Optional[datetime]

    created_at: datetime
    updated_at: datetime
    deleted_at: Optional[datetime]

    class Config:
        orm_mode = True


# Response Schemas
class CostResponse(CostInDB):
    is_overbudget: bool
    variance_percentage: Optional[float]
    days_to_planned_date: int
    execution_status: str

    @validator('is_overbudget', pre=True)
    def calculate_overbudget(cls, v, values):
        actual = values.get('actual_amount')
        estimated = values.get('estimated_amount')
        if actual is None:
            return False
        return actual > estimated

    @validator('variance_percentage', pre=True)
    def calculate_variance_percentage(cls, v, values):
        actual = values.get('actual_amount')
        estimated = values.get('estimated_amount')
        if actual is None or estimated == 0:
            return None
        return round(((actual - estimated) / estimated) * 100, 2)

    @validator('days_to_planned_date', pre=True)
    def calculate_days_to_planned(cls, v, values):
        planned = values.get('planned_date')
        return (planned - date.today()).days

    @validator('execution_status', pre=True)
    def calculate_execution_status(cls, v, values):
        status = values.get('status')
        if status == CostStatus.COMPLETED:
            return "Executed"
        planned = values.get('planned_date')
        if planned < date.today():
            return "Delayed"
        return "On Schedule"


class CostList(BaseModel):
    costs: List[CostResponse]
    total_count: int
    total_estimated: condecimal(max_digits=14, decimal_places=2)
    total_actual: condecimal(max_digits=14, decimal_places=2)
    total_variance: condecimal(max_digits=14, decimal_places=2)


# Document Schema
class CostDocument(BaseModel):
    title: constr(min_length=3, max_length=200)
    document_type: str
    file_path: str
    file_size: int
    mime_type: str
    description: Optional[str] = None
    uploaded_by: str = Field(default="fastapi1403")


# Filter Schema
class CostFilter(BaseModel):
    category: Optional[List[CostCategory]]
    status: Optional[List[CostStatus]]
    priority: Optional[List[CostPriority]]
    date_from: Optional[date]
    date_to: Optional[date]
    min_amount: Optional[condecimal(ge=0)]
    max_amount: Optional[condecimal(ge=0)]
    is_overbudget: Optional[bool]
    tags: Optional[List[str]]
    vendor_id: Optional[int]


# Statistics Schema
class CostStatistics(BaseModel):
    total_costs: int
    total_estimated: condecimal(max_digits=14, decimal_places=2)
    total_actual: condecimal(max_digits=14, decimal_places=2)
    total_variance: condecimal(max_digits=14, decimal_places=2)
    average_variance_percentage: float
    costs_by_category: Dict[CostCategory, Dict[str, Any]]
    costs_by_status: Dict[CostStatus, int]
    monthly_breakdown: List[Dict[str, Any]]
    overbudget_percentage: float
    completion_rate: float

    class Config:
        json_encoders = {
            Decimal: lambda v: float(v)
        }