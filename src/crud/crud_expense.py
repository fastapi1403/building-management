from typing import List, Optional
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from src.models.expense import Expense
from src.schemas.expense import ExpenseCreate, ExpenseUpdate
from src.core.constants import ExpenseCategory
from .base import CRUDBase

class CRUDExpense(CRUDBase[Expense, ExpenseCreate, ExpenseUpdate]):
    async def get_by_category(
        self,
        db: AsyncSession,
        *,
        category: ExpenseCategory,
        start_date: Optional[datetime] = None,
        end_date: Optional[datetime] = None
    ) -> List[Expense]:
        filters = [Expense.category == category]
        if start_date and end_date:
            filters.append(Expense.date.between(start_date, end_date))
        query = select(Expense).where(and_(*filters))
        result = await db.execute(query)
        return result.scalars().all()

crud_expense = CRUDExpense(Expense)
