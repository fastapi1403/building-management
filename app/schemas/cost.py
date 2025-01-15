from datetime import datetime
from decimal import Decimal
from typing import Optional, List
from pydantic import Field
from app.schemas.mixins import BaseSchema
from models.cost import CostType, CostStatus, CostPriority


class CostBase(BaseSchema):
    """Base Cost Schema with common attributes"""
    title: str = Field(
        ...,
        description="Title of the cost",
        min_length=3,
        max_length=100
    )
    description: Optional[str] = Field(
        default=None,
        description="Detailed description of the cost"
    )
    amount: Decimal = Field(
        ...,
        description="Cost amount",
        gt=0,
        decimal_places=2
    )
    cost_type: CostType = Field(
        ...,
        description="Type of the cost"
    )
    status: CostStatus = Field(
        default=CostStatus.DRAFT,
        description="Current status of the cost"
    )
    priority: CostPriority = Field(
        default=CostPriority.MEDIUM,
        description="Priority level of the cost"
    )
    due_date: datetime = Field(
        ...,
        description="Due date for the cost"
    )
    building_id: int = Field(
        ...,
        description="ID of the building this cost belongs to"
    )
    floor_id: Optional[int] = Field(
        default=None,
        description="ID of the floor if cost is floor-specific"
    )
    unit_id: Optional[int] = Field(
        default=None,
        description="ID of the unit if cost is unit-specific"
    )
    vendor_id: Optional[int] = Field(
        default=None,
        description="ID of the vendor if cost is vendor-specific"
    )
    invoice_number: Optional[str] = Field(
        default=None,
        description="Invoice number if available"
    )
    payment_date: Optional[datetime] = Field(
        default=None,
        description="Date when the cost was paid"
    )
    recurring: bool = Field(
        default=False,
        description="Whether this is a recurring cost"
    )
    recurring_period: Optional[str] = Field(
        default=None,
        description="Period for recurring costs (monthly, quarterly, yearly)"
    )
    notes: Optional[str] = Field(
        default=None,
        description="Additional notes or comments"
    )
    tags: List[str] = Field(
        default_factory=list,
        description="Tags for categorizing costs"
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "title": "Monthly Elevator Maintenance",
                "description": "Regular elevator maintenance service",
                "amount": "500.00",
                "cost_type": "maintenance",
                "status": "pending",
                "priority": "medium",
                "due_date": "2025-01-15 14:33:55",
                "building_id": 1,
                "floor_id": None,
                "unit_id": None,
                "vendor_id": 1,
                "invoice_number": "INV-2025-001",
                "payment_date": None,
                "recurring": True,
                "recurring_period": "monthly",
                "tags": ["maintenance", "elevator", "monthly"]
            }
        }


class CostCreate(CostBase):
    """Schema for creating a new cost"""
    pass


class CostUpdate(BaseSchema):
    """Schema for updating an existing cost"""
    title: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=100
    )
    description: Optional[str] = None
    amount: Optional[Decimal] = Field(default=None, gt=0)
    cost_type: Optional[CostType] = None
    status: Optional[CostStatus] = None
    priority: Optional[CostPriority] = None
    due_date: Optional[datetime] = None
    vendor_id: Optional[int] = None
    invoice_number: Optional[str] = None
    payment_date: Optional[datetime] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class CostInDB(CostBase):
    """Schema for cost as stored in database"""
    id: int = Field(..., description="Unique identifier for the cost")


class CostResponse(CostInDB):
    """Schema for cost response"""
    pass


class CostBulkCreate(BaseSchema):
    """Schema for bulk cost creation"""
    costs: List[CostCreate] = Field(
        description="List of costs to create",
        min_length=1
    )

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "costs": [
                    {
                        "title": "Monthly Elevator Maintenance",
                        "description": "Regular elevator maintenance service",
                        "amount": "500.00",
                        "cost_type": "maintenance",
                        "status": "pending",
                        "priority": "medium",
                        "due_date": "2025-01-15 14:33:55",
                        "building_id": 1,
                        "vendor_id": 1,
                        "invoice_number": "INV-2025-001",
                        "recurring": True,
                        "recurring_period": "monthly",
                        "tags": ["maintenance", "elevator", "monthly"]
                    }
                ]
            }
        }


class CostFilter(BaseSchema):
    """Schema for filtering costs"""
    building_id: Optional[int] = None
    floor_id: Optional[int] = None
    unit_id: Optional[int] = None
    vendor_id: Optional[int] = None
    cost_type: Optional[List[CostType]] = None
    status: Optional[List[CostStatus]] = None
    priority: Optional[List[CostPriority]] = None
    date_from: Optional[datetime] = None
    date_to: Optional[datetime] = None
    min_amount: Optional[Decimal] = Field(default=None, gt=0)
    max_amount: Optional[Decimal] = Field(default=None, gt=0)
    recurring: Optional[bool] = None
    tags: Optional[List[str]] = None


class CostStatistics(BaseSchema):
    """Schema for cost statistics"""
    total_costs: int = Field(..., description="Total number of costs")
    total_amount: Decimal = Field(..., description="Total amount of all costs")
    pending_amount: Decimal = Field(..., description="Total amount of pending costs")
    paid_amount: Decimal = Field(..., description="Total amount of paid costs")
    by_type: dict = Field(..., description="Costs grouped by type")
    by_status: dict = Field(..., description="Costs grouped by status")
    by_priority: dict = Field(..., description="Costs grouped by priority")

    class Config:
        json_schema_extra = {
            "example": {
                **BaseSchema.Config.json_schema_extra["example"],
                "total_costs": 150,
                "total_amount": "75000.00",
                "pending_amount": "25000.00",
                "paid_amount": "50000.00",
                "by_type": {
                    "maintenance": {"count": 50, "amount": "25000.00"},
                    "utility": {"count": 100, "amount": "50000.00"}
                },
                "by_status": {
                    "pending": {"count": 30, "amount": "25000.00"},
                    "paid": {"count": 120, "amount": "50000.00"}
                },
                "by_priority": {
                    "high": {"count": 20, "amount": "15000.00"},
                    "medium": {"count": 100, "amount": "45000.00"},
                    "low": {"count": 30, "amount": "15000.00"}
                }
            }
        }