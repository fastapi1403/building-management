from typing import Optional, List
from datetime import date, datetime
from decimal import Decimal
from pydantic import Field, ConfigDict
from app.schemas.mixins import BaseSchema
from app.models.charge import ChargeType, ChargeStatus, ChargeFrequency


class ChargeBase(BaseSchema):
    """Base Charge Schema with common attributes"""
    fund_id: int = Field(..., description="ID of the associated fund")
    name: str = Field(
        ...,
        description="Name of the charge",
        min_length=2,
        max_length=100
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the charge"
    )
    charge_type: ChargeType = Field(
        default=ChargeType.RECURRING,
        description="Type of charge (one-time or recurring)"
    )
    status: ChargeStatus = Field(
        default=ChargeStatus.PENDING,
        description="Current status of the charge"
    )
    amount: Decimal = Field(
        ...,
        description="Amount to be charged",
        gt=0
    )
    frequency: Optional[ChargeFrequency] = Field(
        default=None,
        description="Frequency of recurring charges"
    )
    start_date: date = Field(
        ...,
        description="Start date of the charge"
    )
    end_date: Optional[date] = Field(
        default=None,
        description="End date of the charge (for recurring charges)"
    )
    due_day: Optional[int] = Field(
        default=None,
        description="Day of the month when charge is due",
        ge=1,
        le=31
    )
    grace_period: Optional[int] = Field(
        default=None,
        description="Number of days after due date before late fees apply",
        ge=0
    )
    late_fee: Optional[Decimal] = Field(
        default=None,
        description="Late fee amount",
        ge=0
    )
    late_fee_type: Optional[str] = Field(
        default=None,
        description="Type of late fee (fixed or percentage)"
    )

    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra={
            "example": {
                "fund_id": 1,
                "name": "Monthly Maintenance",
                "description": "Regular monthly maintenance charge",
                "charge_type": "recurring",
                "status": "active",
                "amount": "100.00",
                "frequency": "monthly",
                "start_date": "2024-01-01",
                "due_day": 5,
                "grace_period": 10,
                "late_fee": "10.00",
                "late_fee_type": "fixed"
            }
        }
    )


class ChargeCreate(ChargeBase):
    """Schema for creating a new charge"""
    pass


class ChargeUpdate(BaseSchema):
    """Schema for updating an existing charge"""
    name: Optional[str] = Field(
        default=None,
        min_length=2,
        max_length=100
    )
    description: Optional[str] = None
    charge_type: Optional[ChargeType] = None
    status: Optional[ChargeStatus] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    frequency: Optional[ChargeFrequency] = None
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    due_day: Optional[int] = Field(
        default=None,
        ge=1,
        le=31
    )
    grace_period: Optional[int] = Field(
        default=None,
        ge=0
    )
    late_fee: Optional[Decimal] = Field(
        default=None,
        ge=0
    )
    late_fee_type: Optional[str] = None


class ChargeInDB(ChargeBase):
    """Schema for charge as stored in database"""
    id: int = Field(..., description="Unique identifier for the charge")
    created_at: datetime
    updated_at: datetime


class ChargeResponse(ChargeInDB):
    """Schema for charge response with additional information"""
    fund_name: str = Field(..., description="Name of the associated fund")
    total_units: int = Field(
        default=0,
        description="Total number of units this charge applies to"
    )
    total_amount: Decimal = Field(
        default=Decimal('0.00'),
        description="Total amount to be collected"
    )
    collected_amount: Decimal = Field(
        default=Decimal('0.00'),
        description="Amount already collected"
    )


class ChargeBulkCreate(BaseSchema):
    """Schema for bulk charge creation"""
    charges: List[ChargeCreate] = Field(
        description="List of charges to create",
        min_length=1
    )

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "charges": [
                    {
                        "fund_id": 1,
                        "name": "Monthly Maintenance",
                        "description": "Regular monthly maintenance charge",
                        "charge_type": "recurring",
                        "status": "active",
                        "amount": "100.00",
                        "frequency": "monthly",
                        "start_date": "2024-01-01",
                        "due_day": 5,
                        "grace_period": 10,
                        "late_fee": "10.00",
                        "late_fee_type": "fixed"
                    }
                ]
            }
        }
    )


class ChargeFilter(BaseSchema):
    """Schema for filtering charges"""
    fund_id: Optional[List[int]] = None
    charge_type: Optional[List[ChargeType]] = None
    status: Optional[List[ChargeStatus]] = None
    frequency: Optional[List[ChargeFrequency]] = None
    start_date_from: Optional[date] = None
    start_date_to: Optional[date] = None
    min_amount: Optional[Decimal] = Field(default=None, ge=0)
    max_amount: Optional[Decimal] = Field(default=None, ge=0)
    search: Optional[str] = Field(
        default=None,
        description="Search term for name or description"
    )


class ChargeStatistics(BaseSchema):
    """Schema for charge statistics"""
    total_charges: int = Field(..., description="Total number of charges")
    active_charges: int = Field(..., description="Number of active charges")
    total_amount: Decimal = Field(..., description="Total amount of all charges")
    collected_amount: Decimal = Field(..., description="Total amount collected")
    by_type: dict = Field(..., description="Charges grouped by type")
    by_status: dict = Field(..., description="Charges grouped by status")
    by_frequency: dict = Field(..., description="Charges grouped by frequency")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "total_charges": 100,
                "active_charges": 85,
                "total_amount": "50000.00",
                "collected_amount": "35000.00",
                "by_type": {
                    "recurring": {"count": 80, "amount": "40000.00"},
                    "one_time": {"count": 20, "amount": "10000.00"}
                },
                "by_status": {
                    "active": {"count": 85, "amount": "42500.00"},
                    "inactive": {"count": 15, "amount": "7500.00"}
                },
                "by_frequency": {
                    "monthly": {"count": 60, "amount": "30000.00"},
                    "quarterly": {"count": 20, "amount": "15000.00"},
                    "yearly": {"count": 20, "amount": "5000.00"}
                }
            }
        }
    )