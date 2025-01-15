from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func, text
from datetime import datetime, UTC, timedelta
from decimal import Decimal
import logging

from app.models.fund import Fund, FundTransaction, FundApproval
from app.schemas.fund import (
    FundCreate,
    FundUpdate,
    FundTransaction as TransactionSchema,
    FundApprovalRequest,
    FundFilter
)
from core.exceptions import (
    ResourceNotFoundException,
    DatabaseOperationException,
    InsufficientFundsException,
    BusinessLogicException,
    handle_exceptions
)

logger = logging.getLogger(__name__)


class FundCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, fund_data: FundCreate) -> Fund:
        """Create a new fund"""
        logger.info(f"Creating new fund: {fund_data.name}")

        fund = Fund(
            **fund_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(fund)
            await self.db.commit()
            await self.db.refresh(fund)
            return fund
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail=str(e)
            )

    @handle_exceptions
    async def get(self, fund_id: int) -> Fund:
        """Get fund by ID"""
        query = select(Fund).where(
            and_(
                Fund.id == fund_id,
                Fund.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        fund = result.scalar_one_or_none()

        if not fund:
            raise ResourceNotFoundException(
                resource_type="Fund",
                resource_id=fund_id
            )
        return fund

    @handle_exceptions
    async def update(
            self,
            fund_id: int,
            fund_data: FundUpdate
    ) -> Fund:
        """Update fund information"""
        fund = await self.get(fund_id)
        update_data = fund_data.dict(exclude_unset=True)

        for field, value in update_data.items():
            setattr(fund, field, value)

        fund.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(fund)
            return fund
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail=str(e)
            )

    @handle_exceptions
    async def process_transaction(
            self,
            fund_id: int,
            transaction_data: TransactionSchema
    ) -> FundTransaction:
        """Process a fund transaction"""
        fund = await self.get(fund_id)
        amount = Decimal(str(transaction_data.amount))

        # Validate transaction
        if transaction_data.transaction_type in ["withdrawal", "transfer"]:
            available_balance = fund.current_balance - fund.minimum_balance
            if amount > available_balance:
                raise InsufficientFundsException(
                    required=float(amount),
                    available=float(available_balance)
                )

            if fund.withdrawal_limit and amount > fund.withdrawal_limit:
                raise BusinessLogicException(
                    detail=f"Amount exceeds withdrawal limit of {fund.withdrawal_limit}",
                    code="WITHDRAWAL_LIMIT_EXCEEDED"
                )

        # Create transaction record
        transaction = FundTransaction(
            fund_id=fund_id,
            **transaction_data.dict(),
            balance_after=(
                fund.current_balance + amount
                if transaction_data.transaction_type in ["deposit", "interest"]
                else fund.current_balance - amount
            ),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            # Update fund balance
            if transaction_data.transaction_type in ["deposit", "interest"]:
                fund.current_balance += amount
            else:
                fund.current_balance -= amount

            self.db.add(transaction)
            await self.db.commit()
            await self.db.refresh(transaction)
            return transaction
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="process_transaction",
                detail=str(e)
            )

    @handle_exceptions
    async def create_approval_request(
            self,
            fund_id: int,
            approval_data: FundApprovalRequest
    ) -> FundApproval:
        """Create a new fund approval request"""
        fund = await self.get(fund_id)

        if not fund.requires_approval:
            raise BusinessLogicException(
                detail="This fund does not require approval for transactions",
                code="APPROVAL_NOT_REQUIRED"
            )

        approval = FundApproval(
            fund_id=fund_id,
            **approval_data.dict(),
            status="pending",
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(approval)
            await self.db.commit()
            await self.db.refresh(approval)
            return approval
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create_approval",
                detail=str(e)
            )

    @handle_exceptions
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[FundFilter] = None
    ) -> List[Fund]:
        """Get multiple funds with filtering"""
        query = select(Fund).where(Fund.deleted_at.is_(None))

        if filters:
            if filters.fund_type:
                query = query.where(Fund.fund_type.in_(filters.fund_type))
            if filters.status:
                query = query.where(Fund.status.in_(filters.status))
            if filters.min_balance:
                query = query.where(Fund.current_balance >= filters.min_balance)
            if filters.max_balance:
                query = query.where(Fund.current_balance <= filters.max_balance)
            if filters.requires_approval is not None:
                query = query.where(Fund.requires_approval == filters.requires_approval)
            if filters.tags:
                query = query.where(Fund.tags.contains(filters.tags))

        query = query.order_by(desc(Fund.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def get_statistics(
            self,
            building_id: int,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get fund statistics"""
        # Base query for fund totals
        query = select(
            func.count(Fund.id).label('total_funds'),
            func.sum(Fund.current_balance).label('total_balance'),
            func.sum(Fund.minimum_balance).label('total_minimum')
        ).where(
            and_(
                Fund.building_id == building_id,
                Fund.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(query)
        stats = result.mappings().first()

        # Get transaction statistics
        tx_query = select(
            FundTransaction.transaction_type,
            func.count(FundTransaction.id).label('count'),
            func.sum(FundTransaction.amount).label('total_amount')
        ).join(Fund).where(
            and_(
                Fund.building_id == building_id,
                Fund.deleted_at.is_(None)
            )
        )

        if start_date:
            tx_query = tx_query.where(FundTransaction.created_at >= start_date)
        if end_date:
            tx_query = tx_query.where(FundTransaction.created_at <= end_date)

        tx_query = tx_query.group_by(FundTransaction.transaction_type)
        tx_result = await self.db.execute(tx_query)
        transactions = tx_result.mappings().all()

        return {
            "total_funds": stats.total_funds or 0,
            "total_balance": float(stats.total_balance or 0),
            "total_minimum": float(stats.total_minimum or 0),
            "available_balance": float((stats.total_balance or 0) - (stats.total_minimum or 0)),
            "transactions": {
                tx.transaction_type: {
                    "count": tx.count,
                    "total_amount": float(tx.total_amount or 0)
                }
                for tx in transactions
            }
        }

    @handle_exceptions
    async def get_monthly_report(
            self,
            fund_id: int,
            year: int,
            month: int
    ) -> Dict[str, Any]:
        """Generate monthly fund report"""
        fund = await self.get(fund_id)
        start_date = datetime(year, month, 1, tzinfo=UTC)
        end_date = (
                           start_date + timedelta(days=32)
                   ).replace(day=1) - timedelta(seconds=1)

        # Get transactions for the month
        tx_query = select(FundTransaction).where(
            and_(
                FundTransaction.fund_id == fund_id,
                FundTransaction.created_at.between(start_date, end_date)
            )
        ).order_by(FundTransaction.created_at)

        result = await self.db.execute(tx_query)
        transactions = result.scalars().all()

        return {
            "fund_name": fund.name,
            "period": f"{year}-{month:02d}",
            "opening_balance": float(fund.current_balance),
            "closing_balance": float(fund.current_balance),
            "minimum_balance": float(fund.minimum_balance),
            "transactions": [
                {
                    "date": tx.created_at.isoformat(),
                    "type": tx.transaction_type,
                    "amount": float(tx.amount),
                    "balance_after": float(tx.balance_after),
                    "reference": tx.reference_number
                }
                for tx in transactions
            ]
        }