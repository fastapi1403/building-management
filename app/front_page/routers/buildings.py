from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from crud import crud_building

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/buildings", name="buildings")
async def buildings_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    buildings = await crud_building.get_multi(db=db)
    return templates.TemplateResponse(
        "buildings.html",
        {
            "request": request,
            "buildings": buildings,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/buildings/{building_id}", name="building_details")
async def building_details(
        request: Request,
        building_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Await the building data before passing to template
        building = await crud_building.get(db=db, id=building_id)

        if not building:
            raise HTTPException(status_code=404, detail="Building not found")

        # Get additional data if needed
        # maintenance_history = await crud_building.maintenance.get_building_history(db=db, building_id=building_id)

        # Calculate financial summary
        # total_funds = await crud_building.fund.get_building_total(db=db, building_id=building_id)
        # total_costs = await crud_building.cost.get_building_total(db=db, building_id=building_id)

        # Prepare the context with all required data
        context = {
            "request": request,  # Required by Starlette
            "building": building,
            # "maintenance_history": maintenance_history[:3] if maintenance_history else [],
            # "total_funds": total_funds,
            # "total_costs": total_costs,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "building_detail.html",
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving building details: {str(e)}"
        )