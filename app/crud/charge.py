from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc, Date
from sqlalchemy.orm import joinedload
from datetime import datetime, UTC, date
import logging

from app.models.charge import Charge
from app.models.transaction import Transaction
from app.models.fund import Fund
from app.schemas.charge import (
    ChargeCreate,
    ChargeUpdate,
    ChargeFilter,
    ChargeStatus,
    ChargeStatistics
)
from core.exceptions import (
    ResourceNotFoundException,
    BusinessLogicException,
    DatabaseOperationException,
    handle_exceptions
)

logger = logging.getLogger(__name__)


class ChargeCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, charge_data: ChargeCreate) -> Charge:
        """Create a new charge with validation"""
        logger.info(f"Creating new charge: {charge_data.title}")

        # Validate related entities
        await self._validate_related_entities(
            building_id=charge_data.building_id,
            unit_id=charge_data.unit_id,
            owner_id=charge_data.owner_id,
            tenant_id=charge_data.tenant_id
        )

        charge = Charge(
            **charge_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(charge)
            await self.db.commit()
            await self.db.refresh(charge)

            # Create fund allocation if charge is recurring
            if charge.recurring:
                await self._create_fund_allocation(charge)

            logger.info(f"Successfully created charge with ID: {charge.id}")
            return charge
        except Exception as e:
            logger.error(f"Error creating charge: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail=str(e)
            )

    async def _validate_related_entities(
            self,
            building_id: int,
            unit_id: Optional[int] = None,
            owner_id: Optional[int] = None,
            tenant_id: Optional[int] = None
    ) -> None:
        """Validate all related entities exist"""
        # Implementation depends on your entity relationships
        pass

    async def _create_fund_allocation(self, charge: Charge) -> None:
        """Create fund allocation for recurring charges"""
        # Implementation depends on your fund management logic
        pass

    @handle_exceptions
    async def get(self, charge_id: int) -> Charge:
        """Get a charge by ID"""
        query = (
            select(Charge)
            .options(
                joinedload(Charge.transactions),
                joinedload(Charge.unit),
                joinedload(Charge.owner),
                joinedload(Charge.tenant)
            )
            .where(
                and_(
                    Charge.id == charge_id,
                    Charge.deleted_at.is_(None)
                )
            )
        )

        result = await self.db.execute(query)
        charge = result.scalar_one_or_none()

        if not charge:
            raise ResourceNotFoundException(
                resource_type="Charge",
                resource_id=charge_id
            )
        return charge

    @handle_exceptions
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[ChargeFilter] = None
    ) -> List[Charge]:
        """Get multiple charges with filtering"""
        query = select(Charge).where(Charge.deleted_at.is_(None))

        if filters:
            query = self._apply_filters(query, filters)

        query = query.order_by(desc(Charge.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    def _apply_filters(self, query, filters: ChargeFilter):
        """Apply filters to the query"""
        if filters.status:
            query = query.where(Charge.status.in_(filters.status))
        if filters.type:
            query = query.where(Charge.type.in_(filters.type))
        if filters.due_date_from:
            query = query.where(Charge.due_date >= filters.due_date_from)
        if filters.due_date_to:
            query = query.where(Charge.due_date <= filters.due_date_to)
        if filters.min_amount:
            query = query.where(Charge.amount >= filters.min_amount)
        if filters.max_amount:
            query = query.where(Charge.amount <= filters.max_amount)
        if filters.is_overdue:
            query = query.where(
                and_(
                    Charge.due_date < date.today(),
                    Charge.status != ChargeStatus.PAID
                )
            )
        if filters.unit_id:
            query = query.where(Charge.unit_id == filters.unit_id)
        if filters.owner_id:
            query = query.where(Charge.owner_id == filters.owner_id)
        if filters.tenant_id:
            query = query.where(Charge.tenant_id == filters.tenant_id)
        return query

    @handle_exceptions
    async def update(
            self,
            charge_id: int,
            charge_data: ChargeUpdate
    ) -> Charge:
        """Update charge information"""
        charge = await self.get(charge_id)

        if charge.status == ChargeStatus.PAID:
            raise BusinessLogicException(
                detail="Cannot update a paid charge"
            )

        update_data = charge_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(charge, field, value)

        charge.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(charge)
            return charge
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail=str(e)
            )

    @handle_exceptions
    async def delete(self, charge_id: int) -> bool:
        """Soft delete a charge"""
        charge = await self.get(charge_id)

        if charge.status == ChargeStatus.PAID:
            raise BusinessLogicException(
                detail="Cannot delete a paid charge"
            )

        charge.deleted_at = datetime.now(UTC)
        charge.status = ChargeStatus.CANCELLED

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
    async def record_payment(
            self,
            charge_id: int,
            payment_amount: float,
            payment_reference: str,
            payment_date: datetime = None
    ) -> Charge:
        """Record a payment for a charge"""
        charge = await self.get(charge_id)

        if charge.status == ChargeStatus.PAID:
            raise BusinessLogicException(
                detail="Charge is already paid"
            )

        payment_date = payment_date or datetime.now(UTC)

        # Update charge
        charge.amount_paid += payment_amount
        charge.last_payment_date = payment_date
        charge.payment_reference = payment_reference

        # Update status based on payment
        if charge.amount_paid >= charge.total_amount:
            charge.status = ChargeStatus.PAID
        elif charge.amount_paid > 0:
            charge.status = ChargeStatus.PARTIALLY_PAID

        try:
            await self.db.commit()
            await self.db.refresh(charge)
            return charge
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="payment",
                detail=str(e)
            )

    @handle_exceptions
    async def get_statistics(
            self,
            building_id: int,
            start_date: Optional[date] = None,
            end_date: Optional[date] = None
    ) -> ChargeStatistics:
        """Get charge statistics"""
        query = select(
            func.count(Charge.id).label('total_charges'),
            func.sum(Charge.amount).label('total_amount'),
            func.sum(Charge.amount_paid).label('total_paid'),
            func.count(Charge.id).filter(
                Charge.status == ChargeStatus.OVERDUE
            ).label('overdue_charges')
        ).where(
            and_(
                Charge.building_id == building_id,
                Charge.deleted_at.is_(None)
            )
        )

        if start_date:
            query = query.where(Charge.due_date >= start_date)
        if end_date:
            query = query.where(Charge.due_date <= end_date)

        result = await self.db.execute(query)
        stats = result.one()

        return ChargeStatistics(
            total_charges=stats.total_charges,
            total_amount=stats.total_amount or 0,
            total_paid=stats.total_paid or 0,
            total_pending=stats.total_amount - (stats.total_paid or 0),
            overdue_charges=stats.overdue_charges,
            collection_rate=(stats.total_paid or 0) / stats.total_amount * 100 if stats.total_amount else 0,
            by_type=await self._get_charges_by_type(building_id),
            by_status=await self._get_charges_by_status(building_id),
            monthly_totals=await self._get_monthly_totals(building_id)
        )

    async def _get_charges_by_type(self, building_id: int) -> Dict[str, Any]:
        """Get charges grouped by type"""
        # Implementation for type-based statistics
        pass

    async def _get_charges_by_status(self, building_id: int) -> Dict[str, Any]:
        """Get charges grouped by status"""
        # Implementation for status-based statistics
        pass

    async def _get_monthly_totals(self, building_id: int) -> List[Dict[str, Any]]:
        """Get monthly charge totals"""
        # Implementation for monthly totals
        pass