from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
from src.db.session import get_db
from src.services.report_generator import ReportGenerator

router = APIRouter()
generator = ReportGenerator()

@router.get("/monthly")
async def generate_monthly_report(
    *,
    db: AsyncSession = Depends(get_db),
    month: int,
    year: int,
    format: str = "pdf"
):
    Generate monthly financial report in PDF or Excel format.
    report = await generator.generate_monthly_report(db, month, year, format)
    filename = f"report_{month}_{year}.{format}"
    return FileResponse(
        path=report,
        filename=filename,
        media_type=f"application/{format}"
    )
