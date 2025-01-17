from datetime import datetime

from fastapi import APIRouter, Request, Depends
from fastapi.templating import Jinja2Templates
from sqlmodel import Session

from app.db.session import get_db
from crud import crud_building

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/dashboard", name="dashboard")
async def dashboard_page(
        request: Request,
        db: Session = Depends(get_db)
):
    buildings = await crud_building.get_multi(db=db)

    return templates.TemplateResponse(
        "dashboard.html",
        {
            "request": request,
            "buildings": buildings,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )
