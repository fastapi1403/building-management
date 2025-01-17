from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.crud.building import CRUDBuilding
from app.db.session import get_session

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
crud_building = CRUDBuilding()


@router.get("/dashboard")
async def dashboard_page(
        request: Request,
        db: Session = Depends(get_session)
):
    buildings = await crud_building.get_multi(db=db)
    building_stats = {
        "total": len(buildings),
        "active": len([b for b in buildings if not b.is_deleted]),
        "deleted": len([b for b in buildings if b.is_deleted])
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "buildings": buildings,
            "stats": building_stats,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": "fastapi1403"
        }
    )
