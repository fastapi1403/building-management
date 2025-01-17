from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.crud.building import CRUDBuilding
from app.db.session import get_db

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")
crud_building = CRUDBuilding()


@router.get("/buildings")
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
            "username": "fastapi1403"
        }
    )
