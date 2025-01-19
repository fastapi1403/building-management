from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from crud import crud_floor

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/floors", name="floors")
async def floors_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    floors = await crud_floor.get_multi(db=db)
    return templates.TemplateResponse(
        "floors.html",
        {
            "request": request,
            "floors": floors,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/floors/{floor_id}", name="floor_details")
async def floor_details(
        request: Request,
        floor_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Await the floor data before passing to template
        floor = await crud_floor.get(db=db, id=floor_id)

        if not floor:
            raise HTTPException(status_code=404, detail="Floor not found")

        # Get additional data if needed
        # maintenance_history = await crud_floor.maintenance.get_floor_history(db=db, floor_id=floor_id)

        # Calculate financial summary
        # total_funds = await crud_floor.fund.get_floor_total(db=db, floor_id=floor_id)
        # total_costs = await crud_floor.cost.get_floor_total(db=db, floor_id=floor_id)

        # Prepare the context with all required data
        context = {
            "request": request,  # Required by Starlette
            "floor": floor,
            # "maintenance_history": maintenance_history[:3] if maintenance_history else [],
            # "total_funds": total_funds,
            # "total_costs": total_costs,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "floor_detail.html",
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving floor details: {str(e)}"
        )