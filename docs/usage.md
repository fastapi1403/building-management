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

models/cost.py
```python
# Creating a new maintenance cost
new_cost = Cost(
    title="Annual AC Maintenance",
    description="Regular maintenance of all AC units",
    amount=25000.00,
    estimated_amount=25000.00,
    planned_date=datetime(2025, 2, 1, tzinfo=UTC),
    category=CostCategory.MAINTENANCE,
    priority=CostPriority.MEDIUM,
    building_id=1,
    created_by="fastapi1403",
    is_recurring=True,
    frequency_months=12
)

# Adding a document
document = CostDocument(
    cost_id=new_cost.id,
    title="Maintenance Quote",
    document_type="quote",
    file_path="/documents/costs/2025/quote_123.pdf",
    file_size=156789,
    mime_type="application/pdf",
    uploaded_by="fastapi1403"
)
```

models/fund.py
```python
# Create a new maintenance fund
maintenance_fund = Fund(
    name="Building A Maintenance Fund",
    description="Primary maintenance fund for Building A",
    fund_type=FundType.MAINTENANCE,
    building_id=1,
    current_balance=Decimal('100000.00'),
    minimum_balance=Decimal('20000.00'),
    withdrawal_limit=Decimal('50000.00'),
    manager="fastapi1403",
    created_at=datetime(2025, 1, 15, 12, 5, 16, tzinfo=UTC)
)

# Record a transaction
transaction = FundTransaction(
    fund_id=maintenance_fund.id,
    transaction_type=TransactionType.DEPOSIT,
    amount=Decimal('25000.00'),
    balance_after=Decimal('125000.00'),
    reference_number="DEP-20250115-001",
    description="Monthly maintenance collection",
    initiated_by="fastapi1403",
    transaction_date=datetime(2025, 1, 15, 12, 5, 16, tzinfo=UTC)
)
```

models/transaction.py
```python
# Create a new maintenance payment transaction
new_transaction = Transaction(
    transaction_number="TXN-20250115-001",
    amount=Decimal("5000.00"),
    type=TransactionType.PAYMENT,
    payment_method=PaymentMethod.BANK_TRANSFER,
    building_id=1,
    unit_id=101,
    description="Monthly maintenance payment",
    payment_reference="REF123456",
    bank_reference="BANK789012",
    processed_by="fastapi1403",
    payment_date=datetime(2025, 1, 15, 12, 7, 25, tzinfo=UTC)
)

# Add a transaction split
split = TransactionSplit(
    transaction_id=new_transaction.id,
    amount=Decimal("5000.00"),
    category="maintenance",
    description="Regular maintenance fee",
    fund_id=1
)

# Add a transaction attachment
attachment = TransactionAttachment(
    transaction_id=new_transaction.id,
    file_name="payment_receipt.pdf",
    file_type="application/pdf",
    file_size=125000,
    file_path="/attachments/2025/01/payment_receipt.pdf",
    uploaded_by="fastapi1403",
    description="Payment receipt"
)
```

schemas/charge.py
```python
# Creating a new charge
new_charge = ChargeCreate(
    title="Monthly Maintenance",
    description="Monthly maintenance fee for January 2025",
    amount=Decimal("1500.00"),
    type=ChargeType.MAINTENANCE,
    due_date=date(2025, 1, 31),
    building_id=1,
    unit_id=101,
    is_taxable=True,
    tax_rate=Decimal("18.00"),
    frequency=ChargeFrequency.MONTHLY,
    recurring=True
)

# Updating a charge
charge_update = ChargeUpdate(
    amount=Decimal("1600.00"),
    due_date=date(2025, 2, 1),
    notes="Amount adjusted for inflation"
)

# Recording a payment
payment = ChargePayment(
    amount=Decimal("1500.00"),
    payment_method="bank_transfer",
    payment_reference="REF123456",
    notes="January maintenance payment"
)
```

schemas/cost.py
```python
# Creating a new cost
new_cost = CostCreate(
    title="Annual AC Maintenance",
    description="Preventive maintenance for all AC units",
    category=CostCategory.MAINTENANCE,
    priority=CostPriority.MEDIUM,
    estimated_amount=Decimal("25000.00"),
    planned_date=date(2025, 2, 15),
    building_id=1,
    is_recurring=True,
    frequency_months=12,
    tags=["maintenance", "ac", "yearly"]
)

# Updating a cost
cost_update = CostUpdate(
    status=CostStatus.COMPLETED,
    actual_amount=Decimal("23500.00"),
    completion_date=datetime(2025, 1, 15, 12, 21, 7),
    notes="Completed under budget"
)

# Adding a document
document = CostDocument(
    title="Maintenance Report",
    document_type="report",
    file_path="/documents/2025/01/maintenance_report.pdf",
    file_size=1024000,
    mime_type="application/pdf",
    description="Annual maintenance completion report"
)   
```

schemas/fund.py
```python
# Creating a new fund
new_fund = FundCreate(
    name="Building A Maintenance Fund",
    description="Primary maintenance fund for Building A",
    fund_type=FundType.MAINTENANCE,
    building_id=1,
    current_balance=Decimal("100000.00"),
    minimum_balance=Decimal("20000.00"),
    target_amount=Decimal("500000.00"),
    withdrawal_limit=Decimal("50000.00"),
    tags=["maintenance", "building-a"]
)

# Creating a transaction
transaction = FundTransaction(
    transaction_type=TransactionType.DEPOSIT,
    amount=Decimal("25000.00"),
    reference_number="DEP-20250115-001",
    description="Monthly maintenance collection",
    notes="Regular monthly deposit"
)

# Creating an approval request
approval_request = FundApprovalRequest(
    requested_amount=Decimal("45000.00"),
    purpose="Emergency AC repair",
    justification="Critical repair needed for main AC system",
    supporting_documents=["quote.pdf", "inspection_report.pdf"],
    notes="Urgent approval needed"
)
```

schemas/transaction.py
```python
# Creating a new transaction
new_transaction = TransactionCreate(
    amount=Decimal("5000.00"),
    type=TransactionType.PAYMENT,
    payment_method=PaymentMethod.BANK_TRANSFER,
    description="Monthly maintenance payment",
    building_id=1,
    unit_id=101,
    payment_reference="REF123456",
    bank_reference="BANK789012",
    tags=["maintenance", "monthly"]
)

# Creating a transaction split
split = TransactionSplit(
    amount=Decimal("5000.00"),
    category="maintenance",
    description="Regular maintenance fee",
    fund_id=1
)

# Adding an attachment
attachment = TransactionAttachment(
    file_name="payment_receipt.pdf",
    file_type="application/pdf",
    file_size=156789,
    file_path="/attachments/2025/01/payment_receipt.pdf",
    description="Payment receipt"
)

# Creating a reconciliation record
reconciliation = TransactionReconciliation(
    transaction_id=1,
    reconciled=True,
    notes="Reconciled with bank statement",
    differences=[
        {
            "field": "bank_reference",
            "system_value": "REF123456",
            "bank_value": "REF123456A"
        }
    ]
)
```