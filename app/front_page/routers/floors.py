from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/floors", name="floors")
async def floors_page(request: Request):
    return templates.TemplateResponse(
        "floors.html",
        {
            "request": request,
            "title": "Floors",
            "current_time": "2025-01-19 06:00:21",
        }
    )

@router.get("/floors/{floor_id}", name="floor_details")
async def floor_details(request: Request, floor_id: int):
    return templates.TemplateResponse(
        "floor_detail.html",
        {
            "request": request,
            "floor": {
                "id": floor_id,
                "name": f"Floor {floor_id}",
                "number": floor_id,
                "total_units": 8,
                "occupancy_rate": 75,
                "maintenance_count": 2,
                "is_deleted": False,
            },
            "title": f"Floor {floor_id} Details",
            "current_time": "2025-01-19 06:00:21",
        }
    )