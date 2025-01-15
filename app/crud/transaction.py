from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, desc, func, text
from datetime import datetime, UTC, timedelta
from decimal import Decimal
import logging

from app.models.transaction import (
    Transaction,
    TransactionSplit,
    TransactionAttachment,
    TransactionReconciliation
)
from app.schemas.transaction import (
    TransactionCreate,
    TransactionUpdate,
    TransactionFilter,
    TransactionReconciliation as ReconciliationSchema
)
from core.exceptions import (
    ResourceNotFoundException,
    DatabaseOperationException,
    BusinessLogicException,
    handle_exceptions
)

logger = logging.getLogger(__name__)


class TransactionCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, transaction_data: TransactionCreate) -> Transaction:
        """Create a new transaction"""
        logger.info(f"Creating new transaction of type: {transaction_data.type}")

        # Generate transaction number if not provided
        if not transaction_data.transaction_number:
            timestamp = datetime.now(UTC).strftime("%Y%m%d%H%M%S")
            transaction_data.transaction_number = f"TXN-{timestamp}"

        transaction = Transaction(
            **transaction_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(transaction)
            await self.db.commit()
            await self.db.refresh(transaction)
            return transaction
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail=str(e)
            )

    @handle_exceptions
    async def get(self, transaction_id: int) -> Transaction:
        """Get transaction by ID"""
        query = select(Transaction).where(
            and_(
                Transaction.id == transaction_id,
                Transaction.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        transaction = result.scalar_one_or_none()

        if not transaction:
            raise ResourceNotFoundException(
                resource_type="Transaction",
                resource_id=transaction_id
            )
        return transaction

    @handle_exceptions
    async def update(
            self,
            transaction_id: int,
            transaction_data: TransactionUpdate
    ) -> Transaction:
        """Update transaction information"""
        transaction = await self.get(transaction_id)

        if transaction.status == "completed":
            raise BusinessLogicException(
                detail="Cannot update completed transaction",
                code="COMPLETED_TRANSACTION"
            )

        update_data = transaction_data.dict(exclude_unset=True)

        # Handle status changes
        if "status" in update_data:
            if update_data["status"] == "completed":
                update_data["approved_at"] = datetime.now(UTC)
                update_data["approved_by"] = "fastapi1403"

        for field, value in update_data.items():
            setattr(transaction, field, value)

        transaction.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(transaction)
            return transaction
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail=str(e)
            )

    @handle_exceptions
    async def add_split(
            self,
            transaction_id: int,
            split_data: Dict[str, Any]
    ) -> TransactionSplit:
        """Add a split to a transaction"""
        transaction = await self.get(transaction_id)

        # Validate split amount
        total_splits = await self.get_total_splits(transaction_id)
        new_split_amount = Decimal(str(split_data["amount"]))

        if total_splits + new_split_amount > transaction.amount:
            raise BusinessLogicException(
                detail="Split amount exceeds remaining transaction amount",
                code="INVALID_SPLIT_AMOUNT"
            )

        split = TransactionSplit(
            transaction_id=transaction_id,
            **split_data,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(split)
            await self.db.commit()
            await self.db.refresh(split)
            return split
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="add_split",
                detail=str(e)
            )

    @handle_exceptions
    async def get_total_splits(self, transaction_id: int) -> Decimal:
        """Get total amount of splits for a transaction"""
        query = select(func.sum(TransactionSplit.amount)).where(
            TransactionSplit.transaction_id == transaction_id
        )
        result = await self.db.execute(query)
        return result.scalar() or Decimal("0")

    @handle_exceptions
    async def add_attachment(
            self,
            transaction_id: int,
            attachment_data: Dict[str, Any]
    ) -> TransactionAttachment:
        """Add an attachment to a transaction"""
        transaction = await self.get(transaction_id)

        attachment = TransactionAttachment(
            transaction_id=transaction_id,
            **attachment_data,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(attachment)
            await self.db.commit()
            await self.db.refresh(attachment)
            return attachment
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="add_attachment",
                detail=str(e)
            )

    @handle_exceptions
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[TransactionFilter] = None
    ) -> List[Transaction]:
        """Get multiple transactions with filtering"""
        query = select(Transaction).where(Transaction.deleted_at.is_(None))

        if filters:
            if filters.status:
                query = query.where(Transaction.status.in_(filters.status))
            if filters.type:
                query = query.where(Transaction.type.in_(filters.type))
            if filters.payment_method:
                query = query.where(Transaction.payment_method.in_(filters.payment_method))
            if filters.date_from:
                query = query.where(Transaction.payment_date >= filters.date_from)
            if filters.date_to:
                query = query.where(Transaction.payment_date <= filters.date_to)
            if filters.min_amount:
                query = query.where(Transaction.amount >= filters.min_amount)
            if filters.max_amount:
                query = query.where(Transaction.amount <= filters.max_amount)
            if filters.entity_type and filters.entity_id:
                query = query.where(
                    and_(
                        getattr(Transaction, f"{filters.entity_type}_id") == filters.entity_id
                    )
                )

        query = query.order_by(desc(Transaction.payment_date)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def reconcile(
            self,
            transaction_id: int,
            reconciliation_data: ReconciliationSchema
    ) -> TransactionReconciliation:
        """Reconcile a transaction"""
        transaction = await self.get(transaction_id)

        reconciliation = TransactionReconciliation(
            transaction_id=transaction_id,
            **reconciliation_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(reconciliation)
            await self.db.commit()
            await self.db.refresh(reconciliation)
            return reconciliation
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="reconcile",
                detail=str(e)
            )

    @handle_exceptions
    async def get_statistics(
            self,
            building_id: int,
            start_date: Optional[datetime] = None,
            end_date: Optional[datetime] = None
    ) -> Dict[str, Any]:
        """Get transaction statistics"""
        query = select(
            func.count(Transaction.id).label('total_transactions'),
            func.sum(Transaction.amount).label('total_amount'),
            func.count(case((Transaction.status == 'completed', 1))).label('successful_transactions'),
            func.count(case((Transaction.status == 'failed', 1))).label('failed_transactions')
        ).where(
            and_(
                Transaction.building_id == building_id,
                Transaction.deleted_at.is_(None)
            )
        )

        if start_date:
            query = query.where(Transaction.payment_date >= start_date)
        if end_date:
            query = query.where(Transaction.payment_date <= end_date)

        result = await self.db.execute(query)
        stats = result.mappings().first()

        return {
            "total_transactions": stats.total_transactions or 0,
            "total_amount": float(stats.total_amount or 0),
            "successful_transactions": stats.successful_transactions or 0,
            "failed_transactions": stats.failed_transactions or 0,
            "success_rate": (
                    (stats.successful_transactions or 0) /
                    (stats.total_transactions or 1) * 100
            )
        }