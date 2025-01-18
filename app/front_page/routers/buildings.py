from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db.session import get_db
from crud import crud_building

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/buildings", name="buildings")
async def buildings_page(
        request: Request,
        db: Session = Depends(get_db)
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


@router.get("/buildings/{building_id}", name="building_detail")
async def building_detail(request: Request, building_id: int):
    # Fetch and return building details
    return templates.TemplateResponse(
        "building_detail.html",
        {
            "request": request,
            "building": building
        }
    )