from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from datetime import datetime, date, UTC, timedelta
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

# Configure logger
logger = logging.getLogger(__name__)


class TenantCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, tenant_data: TenantCreate) -> Tenant:
        """
        Create a new tenant with lease validation
        """
        logger.info(f"Creating new tenant for unit {tenant_data.unit_id}")

        # Validate unit availability
        if not await self._is_unit_available(tenant_data.unit_id, None, tenant_data.lease_start_date):
            raise BusinessLogicException(
                detail="Unit is not available for the specified lease period",
                code="UNIT_NOT_AVAILABLE"
            )

        # Validate lease dates
        if tenant_data.lease_end_date <= tenant_data.lease_start_date:
            raise BusinessLogicException(
                detail="Lease end date must be after lease start date",
                code="INVALID_LEASE_DATES"
            )

        tenant = Tenant(
            **tenant_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(tenant)
            # Update unit status
            await self._update_unit_status(tenant_data.unit_id, True)
            await self.db.commit()
            await self.db.refresh(tenant)
            logger.info(f"Successfully created tenant with ID: {tenant.id}")
            return tenant
        except Exception as e:
            logger.error(f"Error creating tenant: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail="Failed to create tenant",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def get(self, tenant_id: int) -> Tenant:
        """
        Get tenant by ID
        """
        logger.info(f"Fetching tenant with ID: {tenant_id}")

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
    async def get_multi(
            self,
            skip: int = 0,
            limit: int = 100,
            filters: Optional[Dict[str, Any]] = None
    ) -> List[Tenant]:
        """
        Get multiple tenants with filtering options
        """
        query = select(Tenant).where(Tenant.deleted_at.is_(None))

        if filters:
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
            if filters.get("active_lease"):
                current_date = datetime.now(UTC).date()
                query = query.where(
                    and_(
                        Tenant.lease_start_date <= current_date,
                        Tenant.lease_end_date >= current_date
                    )
                )
            if filters.get("expiring_soon"):
                days = filters.get("expiring_days", 30)
                future_date = datetime.now(UTC).date() + timedelta(days=days)
                query = query.where(Tenant.lease_end_date <= future_date)

        query = query.order_by(desc(Tenant.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def update(
            self,
            tenant_id: int,
            tenant_data: TenantUpdate
    ) -> Tenant:
        """
        Update tenant information and lease details
        """
        logger.info(f"Updating tenant {tenant_id}")

        tenant = await self.get(tenant_id)
        update_data = tenant_data.dict(exclude_unset=True)

        # Validate lease dates if being updated
        if "lease_end_date" in update_data:
            if update_data["lease_end_date"] <= tenant.lease_start_date:
                raise BusinessLogicException(
                    detail="Lease end date must be after lease start date",
                    code="INVALID_LEASE_DATES"
                )

        # Check unit availability if unit is being changed
        if "unit_id" in update_data:
            if not await self._is_unit_available(
                    update_data["unit_id"],
                    tenant_id,
                    tenant.lease_start_date
            ):
                raise BusinessLogicException(
                    detail="New unit is not available for the specified lease period",
                    code="UNIT_NOT_AVAILABLE"
                )
            # Update old unit status
            await self._update_unit_status(tenant.unit_id, False)
            # Update new unit status
            await self._update_unit_status(update_data["unit_id"], True)

        for field, value in update_data.items():
            setattr(tenant, field, value)

        tenant.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(tenant)
            logger.info(f"Successfully updated tenant {tenant_id}")
            return tenant
        except Exception as e:
            logger.error(f"Error updating tenant {tenant_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail="Failed to update tenant",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def delete(self, tenant_id: int) -> bool:
        """
        Soft delete tenant and update unit status
        """
        logger.info(f"Attempting to delete tenant {tenant_id}")

        tenant = await self.get(tenant_id)

        # Update unit status
        await self._update_unit_status(tenant.unit_id, False)

        tenant.deleted_at = datetime.now(UTC)

        try:
            await self.db.commit()
            logger.info(f"Successfully deleted tenant {tenant_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting tenant {tenant_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="delete",
                detail="Failed to delete tenant"
            )

    async def _is_unit_available(
            self,
            unit_id: int,
            exclude_tenant_id: Optional[int],
            lease_start_date: date
    ) -> bool:
        """
        Check if unit is available for lease
        """
        query = select(Tenant).where(
            and_(
                Tenant.unit_id == unit_id,
                Tenant.deleted_at.is_(None),
                Tenant.lease_end_date >= lease_start_date
            )
        )

        if exclude_tenant_id:
            query = query.where(Tenant.id != exclude_tenant_id)

        result = await self.db.execute(query)
        existing_tenant = result.scalar_one_or_none()
        return existing_tenant is None

    async def _update_unit_status(self, unit_id: int, is_occupied: bool) -> None:
        """
        Update unit occupancy status
        """
        try:
            update_query = (
                Unit.__table__.update()
                .where(Unit.id == unit_id)
                .values(
                    is_occupied=is_occupied,
                    updated_at=datetime.now(UTC)
                )
            )
            await self.db.execute(update_query)
        except Exception as e:
            logger.error(f"Error updating unit status: {str(e)}")
            raise DatabaseOperationException(
                operation="update_unit_status",
                detail="Failed to update unit status"
            )

    @handle_exceptions
    async def get_tenant_statistics(self, tenant_id: int) -> Dict[str, Any]:
        """
        Get comprehensive statistics about a tenant
        """
        tenant = await self.get(tenant_id)
        current_date = datetime.now(UTC).date()

        # Calculate lease statistics
        total_lease_days = (tenant.lease_end_date - tenant.lease_start_date).days
        days_remaining = (tenant.lease_end_date - current_date).days if current_date <= tenant.lease_end_date else 0
        lease_progress = ((total_lease_days - days_remaining) / total_lease_days * 100) if total_lease_days > 0 else 0

        return {
            "tenant_name": tenant.name,
            "tenant_email": tenant.email,
            "unit_id": tenant.unit_id,
            "lease_start": tenant.lease_start_date,
            "lease_end": tenant.lease_end_date,
            "total_lease_days": total_lease_days,
            "days_remaining": days_remaining,
            "lease_progress": round(lease_progress, 2),
            "is_lease_active": tenant.lease_start_date <= current_date <= tenant.lease_end_date,
            "is_lease_expired": current_date > tenant.lease_end_date,
            "days_until_expiry": days_remaining if days_remaining > 0 else 0,
            "tenant_since": tenant.created_at,
            "last_updated": tenant.updated_at
        }

    @handle_exceptions
    async def get_expiring_leases(self, days: int = 30) -> List[Tenant]:
        """
        Get list of tenants whose leases are expiring within specified days
        """
        future_date = datetime.now(UTC).date() + timedelta(days=days)
        current_date = datetime.now(UTC).date()

        query = select(Tenant).where(
            and_(
                Tenant.deleted_at.is_(None),
                Tenant.lease_end_date > current_date,
                Tenant.lease_end_date <= future_date
            )
        ).order_by(Tenant.lease_end_date)

        result = await self.db.execute(query)
        return result.scalars().all()