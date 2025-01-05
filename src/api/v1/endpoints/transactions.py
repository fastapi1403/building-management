from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from src.db.session import get_db
from src.crud import crud_transaction
from src.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionRead

router = APIRouter()

@router.get("/", response_model=List[TransactionRead])
async def get_transactions(
    db: AsyncSession = Depends(get_db),
    transaction_type: Optional[str] = None,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    Retrieve transactions with optional type filter and pagination.
    transactions = await crud_transaction.get_multi(
        db, transaction_type=transaction_type, skip=skip, limit=limit
    )
    return transactions
