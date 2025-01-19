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
        "floors.html",  # You'll need to create this template
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
        # Get floor data
        floor = await crud_floor.get(db=db, id=floor_id)

        if not floor:
            raise HTTPException(status_code=404, detail="Floor not found")

        # Additional data can be added here similar to building details
        # For example:
        # maintenance_records = await crud_floor.maintenance.get_floor_history(db=db, floor_id=floor_id)
        # occupancy_data = await crud_floor.occupancy.get_floor_status(db=db, floor_id=floor_id)

        context = {
            "request": request,
            "floor": floor,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "floor_detail.html",  # You'll need to create this template
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving floor details: {str(e)}"
        )