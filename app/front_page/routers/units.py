from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from crud import crud_unit

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/units", name="units")
async def units_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    units = await crud_unit.get_multi(db=db)
    return templates.TemplateResponse(
        "units.html",
        {
            "request": request,
            "units": units,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/units/{unit_id}", name="unit_details")
async def unit_details(
        request: Request,
        unit_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Await the unit data before passing to template
        unit = await crud_unit.get(db=db, id=unit_id)

        if not unit:
            raise HTTPException(status_code=404, detail="Unit not found")

        # Get additional data if needed
        # maintenance_history = await crud_unit.maintenance.get_unit_history(db=db, unit_id=unit_id)

        # Calculate financial summary
        # total_funds = await crud_unit.fund.get_unit_total(db=db, unit_id=unit_id)
        # total_costs = await crud_unit.cost.get_unit_total(db=db, unit_id=unit_id)

        # Prepare the context with all required data
        context = {
            "request": request,  # Required by Starlette
            "unit": unit,
            # "maintenance_history": maintenance_history[:3] if maintenance_history else [],
            # "total_funds": total_funds,
            # "total_costs": total_costs,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "unit_detail.html",
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving unit details: {str(e)}"
        )