# crud/tenant.py

from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from datetime import datetime, UTC, date
import logging

from app.models.tenant import Tenant
from app.models.unit import Unit
from app.schemas.tenant import TenantCreate, TenantUpdate
from core.exceptions import (
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    BusinessLogicException,
    DatabaseOperationException,
    handle_exceptions
)

logger = logging.getLogger(__name__)


class CRUDTenant:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, tenant_data: TenantCreate) -> Tenant:
        """Create a new tenant with lease validation"""
        logger.info(f"Creating new tenant: {tenant_data.email}")

        # Validate unit availability
        unit_available = await self._check_unit_availability(
            tenant_data.unit_id,
            tenant_data.lease_start_date,
            tenant_data.lease_end_date
        )

        if not unit_available:
            raise BusinessLogicException(
                detail="Unit is not available for the specified lease period",
                code="UNIT_NOT_AVAILABLE"
            )

        # Check for existing active tenant with same email
        existing_tenant = await self.get_by_email(tenant_data.email)
        if existing_tenant and existing_tenant.has_active_lease():
            raise ResourceAlreadyExistsException(
                resource_type="Tenant",
                identifier="email",
                value=tenant_data.email
            )

        tenant = Tenant(
            **tenant_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(tenant)
            # Update unit status
            await self._update_unit_status(tenant_data.unit_id, is_occupied=True)
            await self.db.commit()
            await self.db.refresh(tenant)
            return tenant
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail=str(e)
            )

    async def _check_unit_availability(
            self,
            unit_id: int,
            start_date: date,
            end_date: date
    ) -> bool:
        """Check if unit is available for the specified period"""
        query = select(Tenant).where(
            and_(
                Tenant.unit_id == unit_id,
                Tenant.deleted_at.is_(None),
                or_(
                    and_(
                        Tenant.lease_start_date <= end_date,
                        Tenant.lease_end_date >= start_date
                    )
                )
            )
        )
        result = await self.db.execute(query)
        existing_lease = result.scalar_one_or_none()
        return existing_lease is None

    async def _update_unit_status(self, unit_id: int, is_occupied: bool):
        """Update unit occupancy status"""
        query = (
            Unit.__table__.update()
            .where(Unit.id == unit_id)
            .values(
                is_occupied=is_occupied,
                updated_at=datetime.now(UTC)
            )
        )
        await self.db.execute(query)

    @handle_exceptions
    async def get(self, tenant_id: int) -> Tenant:
        """Get tenant by ID"""
        query = select(Tenant).where(
            and_(
                Tenant.id == tenant_id,
                Tenant.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        tenant = result.scalar_one_or_none()

        if not tenant:
            raise ResourceNotFoundException(
                resource_type="Tenant",
                resource_id=tenant_id
            )
        return tenant

    @handle_exceptions
    async def get_by_email(self, email: str) -> Optional[Tenant]:
        """Get tenant by email"""
        query = select(Tenant).where(
            and_(
                Tenant.email == email,
                Tenant.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    @handle_exceptions
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Tenant]:
        """Get multiple tenants with filtering"""
        query = select(Tenant).where(Tenant.deleted_at.is_(None))

        if filters:
            if filters.get("active_only"):
                current_date = datetime.now(UTC).date()
                query = query.where(
                    and_(
                        Tenant.lease_start_date <= current_date,
                        Tenant.lease_end_date >= current_date
                    )
                )
            if filters.get("search"):
                search_term = f"%{filters['search']}%"
                query = query.where(
                    or_(
                        Tenant.name.ilike(search_term),
                        Tenant.email.ilike(search_term)
                    )
                )
            if filters.get("unit_id"):
                query = query.where(Tenant.unit_id == filters["unit_id"])

        query = query.order_by(desc(Tenant.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def update(
            self,
            tenant_id: int,
            tenant_data: TenantUpdate
    ) -> Tenant:
        """Update tenant information"""
        tenant = await self.get(tenant_id)
        update_data = tenant_data.dict(exclude_unset=True)

        if "lease_end_date" in update_data:
            # Validate new lease end date
            if update_data["lease_end_date"] <= datetime.now(UTC).date():
                raise BusinessLogicException(
                    detail="Lease end date must be in the future"
                )

        for field, value in update_data.items():
            setattr(tenant, field, value)

        tenant.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(tenant)
            return tenant
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail=str(e)
            )

    @handle_exceptions
    async def delete(self, tenant_id: int) -> bool:
        """Soft delete tenant and update unit status"""
        tenant = await self.get(tenant_id)

        tenant.deleted_at = datetime.now(UTC)
        await self._update_unit_status(tenant.unit_id, is_occupied=False)

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
    async def get_tenant_history(self, tenant_id: int) -> List[Dict[str, Any]]:
        """Get tenant's lease history"""
        query = select(
            Tenant.unit_id,
            Tenant.lease_start_date,
            Tenant.lease_end_date,
            Unit.unit_number
        ).join(Unit).where(
            and_(
                Tenant.id == tenant_id,
                Tenant.deleted_at.is_(None)
            )
        ).order_by(desc(Tenant.lease_start_date))

        result = await self.db.execute(query)
        return [
            {
                "unit_number": row.unit_number,
                "lease_start": row.lease_start_date,
                "lease_end": row.lease_end_date,
                "unit_id": row.unit_id
            }
            for row in result
        ]

    @handle_exceptions
    async def extend_lease(
            self,
            tenant_id: int,
            new_end_date: date
    ) -> Tenant:
        """Extend tenant's lease"""
        tenant = await self.get(tenant_id)

        if new_end_date <= tenant.lease_end_date:
            raise BusinessLogicException(
                detail="New end date must be after current lease end date"
            )

        # Validate unit availability for extension
        unit_available = await self._check_unit_availability(
            tenant.unit_id,
            tenant.lease_end_date,
            new_end_date
        )

        if not unit_available:
            raise BusinessLogicException(
                detail="Unit is not available for lease extension"
            )

        tenant.lease_end_date = new_end_date
        tenant.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(tenant)
            return tenant
        except Exception as e:
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="extend_lease",
                detail=str(e)
            )