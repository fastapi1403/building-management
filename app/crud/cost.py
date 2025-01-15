from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func
from datetime import datetime, UTC
import logging

from app.models.cost import Cost, CostDocument
from app.schemas.cost import CostCreate, CostUpdate, CostFilter
from core.exceptions import (
    ResourceNotFoundException,
    DatabaseOperationException,
    BusinessLogicException,
    handle_exceptions
)

logger = logging.getLogger(__name__)


class CostCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, cost_data: CostCreate) -> Cost:
        """Create a new cost record"""
        logger.info(f"Creating new cost: {cost_data.title}")

        cost = Cost(
            **cost_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(cost)
            await self.db.commit()
            await self.db.refresh(cost)
            return cost
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail=str(e)
            )

    @handle_exceptions
    async def get(self, cost_id: int) -> Cost:
        """Get cost by ID"""
        query = select(Cost).where(
            and_(
                Cost.id == cost_id,
                Cost.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        cost = result.scalar_one_or_none()

        if not cost:
            raise ResourceNotFoundException(
                resource_type="Cost",
                resource_id=cost_id
            )
        return cost

    @handle_exceptions
    async def update(
            self,
            cost_id: int,
            cost_data: CostUpdate
    ) -> Cost:
        """Update cost information"""
        cost = await self.get(cost_id)
        update_data = cost_data.dict(exclude_unset=True)

        if "actual_amount" in update_data and update_data["actual_amount"]:
            cost.variance_amount = (
                    update_data["actual_amount"] - cost.estimated_amount
            )

        for field, value in update_data.items():
            setattr(cost, field, value)

        cost.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(cost)
            return cost
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail=str(e)
            )

    @handle_exceptions
    async def delete(self, cost_id: int) -> bool:
        """Soft delete cost"""
        cost = await self.get(cost_id)
        cost.deleted_at = datetime.now(UTC)

        try:
            await self.db.commit()
            return True
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="delete",
                detail=str(e)
            )

    @handle_exceptions
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[CostFilter] = None
    ) -> List[Cost]:
        """Get multiple costs with filtering"""
        query = select(Cost).where(Cost.deleted_at.is_(None))

        if filters:
            if filters.category:
                query = query.where(Cost.category.in_(filters.category))
            if filters.status:
                query = query.where(Cost.status.in_(filters.status))
            if filters.priority:
                query = query.where(Cost.priority.in_(filters.priority))
            if filters.date_from:
                query = query.where(Cost.planned_date >= filters.date_from)
            if filters.date_to:
                query = query.where(Cost.planned_date <= filters.date_to)
            if filters.min_amount:
                query = query.where(Cost.estimated_amount >= filters.min_amount)
            if filters.max_amount:
                query = query.where(Cost.estimated_amount <= filters.max_amount)
            if filters.vendor_id:
                query = query.where(Cost.vendor_id == filters.vendor_id)
            if filters.tags:
                query = query.where(Cost.tags.contains(filters.tags))

        query = query.order_by(desc(Cost.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    async def add_document(
            self,
            cost_id: int,
            document_data: Dict[str, Any]
    ) -> CostDocument:
        """Add a document to a cost"""
        cost = await self.get(cost_id)
        document = CostDocument(
            cost_id=cost.id,
            **document_data,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(document)
            await self.db.commit()
            await self.db.refresh(document)
            return document
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="add_document",
                detail=str(e)
            )

    @handle_exceptions
    async def get_statistics(
            self,
            building_id: int,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get cost statistics for a building"""
        query = select(
            func.count(Cost.id).label('total_costs'),
            func.sum(Cost.estimated_amount).label('total_estimated'),
            func.sum(Cost.actual_amount).label('total_actual'),
            func.avg(
                (Cost.actual_amount - Cost.estimated_amount) /
                Cost.estimated_amount * 100
            ).label('avg_variance_percentage')
        ).where(
            and_(
                Cost.building_id == building_id,
                Cost.deleted_at.is_(None)
            )
        )

        if start_date:
            query = query.where(Cost.planned_date >= start_date)
        if end_date:
            query = query.where(Cost.planned_date <= end_date)

        result = await self.db.execute(query)
        stats = result.mappings().first()

        # Get category breakdown
        category_query = select(
            Cost.category,
            func.count(Cost.id).label('count'),
            func.sum(Cost.estimated_amount).label('total_estimated'),
            func.sum(Cost.actual_amount).label('total_actual')
        ).where(
            and_(
                Cost.building_id == building_id,
                Cost.deleted_at.is_(None)
            )
        ).group_by(Cost.category)

        category_result = await self.db.execute(category_query)
        categories = category_result.mappings().all()

        return {
            "total_costs": stats.total_costs or 0,
            "total_estimated": float(stats.total_estimated or 0),
            "total_actual": float(stats.total_actual or 0),
            "avg_variance_percentage": float(stats.avg_variance_percentage or 0),
            "by_category": {
                cat.category: {
                    "count": cat.count,
                    "total_estimated": float(cat.total_estimated or 0),
                    "total_actual": float(cat.total_actual or 0)
                }
                for cat in categories
            }
        }

    @handle_exceptions
    async def mark_completed(
            self,
            cost_id: int,
            actual_amount: float,
            completion_date: Optional[datetime] = None
    ) -> Cost:
        """Mark a cost as completed with actual amount"""
        cost = await self.get(cost_id)

        if cost.status == "completed":
            raise BusinessLogicException(
                detail="Cost is already marked as completed",
                code="ALREADY_COMPLETED"
            )

        update_data = {
            "status": "completed",
            "actual_amount": actual_amount,
            "completion_date": completion_date or datetime.now(UTC),
            "variance_amount": actual_amount - float(cost.estimated_amount)
        }

        try:
            for field, value in update_data.items():
                setattr(cost, field, value)
            cost.updated_at = datetime.now(UTC)
            await self.db.commit()
            await self.db.refresh(cost)
            return cost
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="mark_completed",
                detail=str(e)
            )