crud/floor.py
```python
async def get_floor_details(
    floor_id: int,
    db: AsyncSession = Depends(get_db)
):
    floor_crud = FloorCRUD(db)
    floor = await floor_crud.get(floor_id)
    stats = await floor_crud.get_floor_statistics(floor_id)
    return {
        "floor": floor,
        "statistics": stats
    }
```

core/exceptions.py
```python
from core.exceptions import handle_exceptions, ResourceNotFoundException

class BuildingService:
    @handle_exceptions
    async def get_building(self, building_id: int):
        building = await self.repository.get(building_id)
        if not building:
            raise ResourceNotFoundException(
                resource_type="Building",
                resource_id=building_id,
                metadata={"requested_at": datetime.utcnow()}
            )
        return building
```
crud/owner.py
```python
from typing import List, Optional, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, or_, func, desc
from datetime import datetime, UTC
import logging

from app.models.owner import Owner
from app.models.unit import Unit
from app.schemas.owner import OwnerCreate, OwnerUpdate
from core.exceptions import (
    ResourceNotFoundException,
    ResourceAlreadyExistsException,
    BusinessLogicException,
    DatabaseOperationException,
    handle_exceptions
)

# Configure logger
logger = logging.getLogger(__name__)

class OwnerCRUD:
    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    @handle_exceptions
    async def create(self, owner_data: OwnerCreate) -> Owner:
        """
        Create a new owner with validation
        """
        logger.info(f"Creating new owner: {owner_data.email}")

        # Check if owner with email already exists
        existing_owner = await self.get_by_email(owner_data.email)
        if existing_owner:
            logger.error(f"Owner with email {owner_data.email} already exists")
            raise ResourceAlreadyExistsException(
                resource_type="Owner",
                identifier="email",
                value=owner_data.email,
                metadata={"attempted_at": datetime.now(UTC)}
            )

        owner = Owner(
            **owner_data.dict(),
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC)
        )

        try:
            self.db.add(owner)
            await self.db.commit()
            await self.db.refresh(owner)
            logger.info(f"Successfully created owner with ID: {owner.id}")
            return owner
        except Exception as e:
            logger.error(f"Error creating owner: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="create",
                detail="Failed to create owner",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def get(self, owner_id: int) -> Owner:
        """
        Get owner by ID
        """
        logger.info(f"Fetching owner with ID: {owner_id}")

        query = select(Owner).where(
            and_(
                Owner.id == owner_id,
                Owner.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(query)
        owner = result.scalar_one_or_none()

        if not owner:
            raise ResourceNotFoundException(
                resource_type="Owner",
                resource_id=owner_id
            )

        return owner

    @handle_exceptions
    async def get_by_email(self, email: str) -> Optional[Owner]:
        """
        Get owner by email
        """
        query = select(Owner).where(
            and_(
                Owner.email == email,
                Owner.deleted_at.is_(None)
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
    ) -> List[Owner]:
        """
        Get multiple owners with filtering options
        """
        query = select(Owner).where(Owner.deleted_at.is_(None))

        if filters:
            if filters.get("search"):
                search_term = f"%{filters['search']}%"
                query = query.where(
                    or_(
                        Owner.name.ilike(search_term),
                        Owner.email.ilike(search_term)
                    )
                )
            if filters.get("has_units"):
                query = query.join(Unit).group_by(Owner.id)

        query = query.order_by(desc(Owner.created_at)).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def update(
        self,
        owner_id: int,
        owner_data: OwnerUpdate
    ) -> Owner:
        """
        Update owner information
        """
        logger.info(f"Updating owner {owner_id}")

        owner = await self.get(owner_id)
        update_data = owner_data.dict(exclude_unset=True)

        if "email" in update_data and update_data["email"] != owner.email:
            existing_owner = await self.get_by_email(update_data["email"])
            if existing_owner:
                raise ResourceAlreadyExistsException(
                    resource_type="Owner",
                    identifier="email",
                    value=update_data["email"]
                )

        for field, value in update_data.items():
            setattr(owner, field, value)

        owner.updated_at = datetime.now(UTC)

        try:
            await self.db.commit()
            await self.db.refresh(owner)
            logger.info(f"Successfully updated owner {owner_id}")
            return owner
        except Exception as e:
            logger.error(f"Error updating owner {owner_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="update",
                detail="Failed to update owner",
                metadata={"error": str(e)}
            )

    @handle_exceptions
    async def delete(self, owner_id: int) -> bool:
        """
        Soft delete owner with validation
        """
        logger.info(f"Attempting to delete owner {owner_id}")

        owner = await self.get(owner_id)
        
        # Check if owner has any active units
        active_units = await self.get_owner_active_units(owner_id)
        if active_units:
            raise BusinessLogicException(
                detail="Cannot delete owner with active units",
                metadata={"active_units": len(active_units)}
            )

        owner.deleted_at = datetime.now(UTC)

        try:
            await self.db.commit()
            logger.info(f"Successfully deleted owner {owner_id}")
            return True
        except Exception as e:
            logger.error(f"Error deleting owner {owner_id}: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="delete",
                detail="Failed to delete owner"
            )

    @handle_exceptions
    async def get_owner_active_units(self, owner_id: int) -> List[Unit]:
        """
        Get all active units owned by an owner
        """
        query = select(Unit).where(
            and_(
                Unit.current_owner_id == owner_id,
                Unit.deleted_at.is_(None)
            )
        )
        result = await self.db.execute(query)
        return result.scalars().all()

    @handle_exceptions
    async def get_owner_statistics(self, owner_id: int) -> Dict[str, Any]:
        """
        Get comprehensive statistics about an owner
        """
        owner = await self.get(owner_id)
        
        # Get units statistics
        units_query = select(
            func.count(Unit.id).label('total_units'),
            func.count(Unit.id).filter(Unit.is_occupied.is_(True)).label('occupied_units'),
            func.sum(Unit.area_sqft).label('total_area'),
            func.sum(Unit.monthly_maintenance).label('total_maintenance')
        ).where(
            and_(
                Unit.current_owner_id == owner_id,
                Unit.deleted_at.is_(None)
            )
        )

        result = await self.db.execute(units_query)
        stats = result.one()

        return {
            "owner_name": owner.name,
            "owner_email": owner.email,
            "total_units": stats.total_units or 0,
            "occupied_units": stats.occupied_units or 0,
            "vacancy_rate": ((stats.total_units - stats.occupied_units) / stats.total_units * 100) 
                          if stats.total_units else 0,
            "total_area_owned": round(stats.total_area or 0, 2),
            "total_monthly_maintenance": round(stats.total_maintenance or 0, 2),
            "member_since": owner.created_at,
            "last_updated": owner.updated_at
        }

    @handle_exceptions
    async def transfer_units(
        self,
        from_owner_id: int,
        to_owner_id: int,
        unit_ids: List[int]
    ) -> bool:
        """
        Transfer units from one owner to another
        """
        logger.info(f"Transferring units {unit_ids} from owner {from_owner_id} to {to_owner_id}")

        from_owner = await self.get(from_owner_id)
        to_owner = await self.get(to_owner_id)

        try:
            # Update units ownership
            update_query = (
                Unit.__table__.update()
                .where(
                    and_(
                        Unit.id.in_(unit_ids),
                        Unit.current_owner_id == from_owner_id
                    )
                )
                .values(
                    current_owner_id=to_owner_id,
                    updated_at=datetime.now(UTC)
                )
            )

            await self.db.execute(update_query)
            await self.db.commit()
            
            logger.info(f"Successfully transferred units from owner {from_owner_id} to {to_owner_id}")
            return True
        except Exception as e:
            logger.error(f"Error transferring units: {str(e)}")
            await self.db.rollback()
            raise DatabaseOperationException(
                operation="transfer",
                detail="Failed to transfer units",
                metadata={
                    "from_owner": from_owner_id,
                    "to_owner": to_owner_id,
                    "units": unit_ids
                }
            )
```

crud/tenant.py
```python
async def get_expiring_leases(
    days: int = 30,
    db: AsyncSession = Depends(get_db)
):
    tenant_crud = TenantCRUD(db)
    expiring_leases = await tenant_crud.get_expiring_leases(days)
    return [
        {
            "tenant": tenant,
            "stats": await tenant_crud.get_tenant_statistics(tenant.id)
        }
        for tenant in expiring_leases
    ]
```

models/charge.py
```python
# Creating a new maintenance charge
new_charge = Charge(
    title="Monthly Maintenance",
    description="Monthly maintenance fee for January 2025",
    amount=1500.00,
    due_date=datetime(2025, 1, 31, tzinfo=UTC),
    building_id=1,
    unit_id=101,
    generated_by="system",
    type=ChargeType.MAINTENANCE,
    frequency=ChargeFrequency.MONTHLY,
    recurring=True
)

# Recording a payment
payment = Payment(
    charge_id=new_charge.id,
    amount=1500.00,
    payment_method="bank_transfer",
    transaction_id="TXN123456",
    notes="January 2025 maintenance payment"
)
```