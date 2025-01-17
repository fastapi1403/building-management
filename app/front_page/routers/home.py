from datetime import datetime

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from app.crud.building import CRUDBuilding

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")
crud_building = CRUDBuilding()


@router.get("/")
async def home_page(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": "fastapi1403"
        }
    )
