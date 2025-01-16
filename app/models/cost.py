from datetime import datetime, UTC
from typing import Optional, List
from enum import Enum
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column, String, Enum as SQLEnum, Index

from app.models.mixins import SoftDeleteMixin, TimestampMixin

# from mixins import TimestampMixin, SoftDeleteMixin
# # Type annotations for relationships
# from .building import Building
# from .unit import Unit
# from .floor import Floor


class CostType(str, Enum):
    """Enum for cost categories"""
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
    """Enum for cost priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class CostStatus(str, Enum):
    """Enum for cost status"""
    PLANNED = "planned"
    APPROVED = "approved"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"
    DRAFT = "draft"
    PENDING = "pending"
    REJECTED = "rejected"
    PAID = "paid"
    REFUNDED = "refunded"


class Cost(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    """
    Model for tracking costs and expenses in the building management system
    """
    __tablename__ = "costs"

    id: Optional[int] = Field(default=None, primary_key=True)

    # Basic cost information
    title: str = Field(..., max_length=200)
    description: str = Field(..., max_length=1000)
    amount: float = Field(..., gt=0)

    # Classification
    cost_type: CostType = Field(
        sa_column=Column(SQLEnum(CostType)),
        default=CostType.MAINTENANCE
    )
    priority: CostPriority = Field(
        sa_column=Column(SQLEnum(CostPriority)),
        default=CostPriority.MEDIUM
    )
    status: CostStatus = Field(
        sa_column=Column(SQLEnum(CostStatus)),
        default=CostStatus.PLANNED
    )

    # Timing
    planned_date: datetime = Field(...)
    actual_date: Optional[datetime] = Field(default=None)
    completion_date: Optional[datetime] = Field(default=None)

    # Financial tracking
    estimated_amount: float = Field(..., gt=0)
    actual_amount: Optional[float] = Field(default=None)
    variance_amount: Optional[float] = Field(default=None)
    budget_code: Optional[str] = Field(default=None, max_length=50)

    # Related entities
    building_id: int = Field(..., foreign_key="buildings.id")
    unit_id: Optional[int] = Field(default=None, foreign_key="units.id")
    floor_id: Optional[int] = Field(default=None, foreign_key="floors.id")
    vendor_id: Optional[int] = Field(default=None, foreign_key="vendors.id")

    # Additional metadata
    is_recurring: bool = Field(default=False)
    frequency_months: Optional[int] = Field(default=None)
    warranty_expires: Optional[datetime] = Field(default=None)
    invoice_number: Optional[str] = Field(default=None, max_length=50)
    purchase_order: Optional[str] = Field(default=None, max_length=50)
    notes: Optional[str] = Field(default=None, max_length=1000)
    tags: List[str] = Field(default_factory=list)

    # Relationships
    building: "Building" = Relationship(back_populates="costs")
    unit: Optional["Unit"] = Relationship(back_populates="costs")
    floor: Optional["Floor"] = Relationship(back_populates="costs")
    documents: List["CostDocument"] = Relationship(back_populates="cost")

    # Indexes for better query performance
    __table_args__ = (
        Index('ix_costs_category_status', 'category', 'status'),
        Index('ix_costs_planned_date', 'planned_date'),
        Index('ix_costs_building_id', 'building_id'),
    )

    class Config:
        arbitrary_types_allowed = True

    @property
    def is_overburden(self) -> bool:
        """Check if actual cost exceeds estimated cost"""
        if self.actual_amount is None:
            return False
        return self.actual_amount > self.estimated_amount

    @property
    def variance_percentage(self) -> Optional[float]:
        """Calculate variance percentage from estimated cost"""
        if self.actual_amount is None or self.estimated_amount == 0:
            return None
        return round(((self.actual_amount - self.estimated_amount) / self.estimated_amount) * 100, 2)

    def update_variance(self) -> None:
        """Update variance amount based on actual and estimated costs"""
        if self.actual_amount is not None:
            self.variance_amount = round(self.actual_amount - self.estimated_amount, 2)

    def mark_completed(self, actual_amount: float, completion_date: datetime = None) -> None:
        """Mark cost as completed with actual amount"""
        self.status = CostStatus.COMPLETED
        self.actual_amount = actual_amount
        self.completion_date = completion_date or datetime.now(UTC)
        self.update_variance()


class CostDocument(SoftDeleteMixin, TimestampMixin, SQLModel, table=True):
    """
    Model for storing documents related to costs (invoices, receipts, etc.)
    """
    __tablename__ = "cost_documents"

    id: Optional[int] = Field(default=None, primary_key=True)
    cost_id: int = Field(..., foreign_key="costs.id")

    # Document information
    title: str = Field(..., max_length=200)
    document_type: str = Field(..., max_length=50)  # invoice, receipt, quote, etc.
    file_path: str = Field(..., max_length=500)
    file_size: int = Field(...)  # in bytes
    mime_type: str = Field(..., max_length=100)

    # Metadata
    description: Optional[str] = Field(default=None, max_length=500)

    # Relationship
    cost: Cost = Relationship(back_populates="documents")

    class Config:
        arbitrary_types_allowed = True

Cost.model_rebuild()
CostDocument.model_rebuild()