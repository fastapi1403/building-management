from datetime import datetime, UTC
from decimal import Decimal
from typing import Optional, List

from pydantic import Field

from app.schemas.mixins import BaseSchema
from app.models.charge import ChargeStatus, ChargeType


class ChargeBase(BaseSchema):
    """Base Charge Schema with common attributes"""
    title: str = Field(...,
                       description="Title of the charge",
                       min_length=3,
                       max_length=100
                       )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the charge"
    )
    amount: Decimal = Field(...,
                            description="Amount to be charged",
                            gt=0,
                            decimal_places=2
                            )
    charge_type: ChargeType = Field(...,
                                    description="Type of the charge"
                                    )
    due_date: datetime = Field(...,
                               description="Due date for the charge"
                               )
    status: ChargeStatus = Field(
        default=ChargeStatus.PENDING,
        description="Current status of the charge"
    )
    building_id: int = Field(...,
                             description="ID of the building this charge belongs to"
                             )
    unit_id: Optional[int] = Field(
        default=None,
        description="ID of the unit if charge is unit-specific"
    )
    floor_id: Optional[int] = Field(
        default=None,
        description="ID of the floor if charge is floor-specific"
    )
    recurring: bool = Field(
        default=False,
        description="Whether this is a recurring charge"
    )
    recurring_period: Optional[str] = Field(
        default=None,
        description="Period for recurring charges (monthly, quarterly, yearly)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes or comments"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorizing charges"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "title": "Monthly Maintenance Fee",
                "description": "Regular maintenance charge for January 2025",
                "amount": "150.00",
                "charge_type": "maintenance",
                "due_date": "2025-01-31T00:00:00Z",
                "status": "pending",
                "building_id": 1,
                "unit_id": 101,
                "recurring": True,
                "recurring_period": "monthly",
                "tags": ["maintenance", "monthly"]
            }
        }


class ChargeCreate(ChargeBase):
    """Schema for creating a new charge"""
    created_by: str = Field(default="fastapi1403")
    updated_by: str = Field(default="fastapi1403")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChargeUpdate(BaseSchema):
    """Schema for updating an existing charge"""
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    charge_type: Optional[ChargeType] = None
    due_date: Optional[datetime] = None
    status: Optional[ChargeStatus] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None
    updated_by: str = Field(default="fastapi1403")
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class ChargeInDB(ChargeBase):
    """Schema for charge as stored in database"""
    id: int = Field(..., description="Unique identifier for the charge")


class ChargeResponse(ChargeInDB):
    """Schema for charge response"""
    pass


class ChargeBulkCreate(BaseSchema):
    """Schema for bulk charge creation"""
    charges: List[ChargeCreate] = Field(
        description="List of charges to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "charges": [
                    {
                        "title": "Monthly Maintenance Fee",
                        "description": "Regular maintenance charge for January 2025",
                        "amount": "150.00",
                        "charge_type": "maintenance",
                        "due_date": "2025-01-15 14:24:22",
                        "status": "pending",
                        "building_id": 1,
                        "unit_id": 101,
                        "recurring": True,
                        "recurring_period": "monthly",
                        "tags": ["maintenance", "monthly"],
                        "created_by": "fastapi1403",
                        "updated_by": "fastapi1403"
                    }
                ]
            }
        }

class ChargeFilter(BaseSchema):
    """Schema for filtering charges"""
    building_id: Optional[int] = None
    unit_id: Optional[int] = None
    floor_id: Optional[int] = None
    charge_type: Optional[List[ChargeType]] = None
    status: Optional[List[ChargeStatus]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[Decimal] = Field(default=None, gt=0)
    max_amount: Optional[Decimal] = Field(default=None, gt=0)
    recurring: Optional[bool] = None
    tags: Optional[List[str]] = None


class ChargeStatistics(BaseSchema):
    """Schema for charge statistics"""
    total_charges: int = Field(..., description="Total number of charges")
    total_amount: Decimal = Field(..., description="Total amount of all charges")
    pending_amount: Decimal = Field(..., description="Total amount of pending charges")
    overdue_amount: Decimal = Field(..., description="Total amount of overdue charges")
    paid_amount: Decimal = Field(..., description="Total amount of paid charges")
    by_type: dict = Field(..., description="Charges grouped by type")
    by_status: dict = Field(..., description="Charges grouped by status")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_charges": 150,
                "total_amount": "25000.00",
                "pending_amount": "5000.00",
                "overdue_amount": "1000.00",
                "paid_amount": "19000.00",
                "by_type": {
                    "maintenance": {"count": 50, "amount": "10000.00"},
                    "utility": {"count": 100, "amount": "15000.00"}
                },
                "by_status": {
                    "pending": {"count": 20, "amount": "5000.00"},
                    "paid": {"count": 130, "amount": "20000.00"}
                }
            }
        }
