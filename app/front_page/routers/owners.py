from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from crud import crud_owner

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/owners", name="owners")
async def owners_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    owners = await crud_owner.get_multi(db=db)
    return templates.TemplateResponse(
        "owners.html",
        {
            "request": request,
            "owners": owners,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/owners/{owner_id}", name="owner_details")
async def owner_details(
        request: Request,
        owner_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Await the owner data before passing to template
        owner = await crud_owner.get(db=db, id=owner_id)

        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")

        # Get additional data if needed
        # maintenance_history = await crud_owner.maintenance.get_owner_history(db=db, owner_id=owner_id)

        # Calculate financial summary
        # total_funds = await crud_owner.fund.get_owner_total(db=db, owner_id=owner_id)
        # total_costs = await crud_owner.cost.get_owner_total(db=db, owner_id=owner_id)

        # Prepare the context with all required data
        context = {
            "request": request,  # Required by Starlette
            "owner": owner,
            # "maintenance_history": maintenance_history[:3] if maintenance_history else [],
            # "total_funds": total_funds,
            # "total_costs": total_costs,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "owner_detail.html",
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving owner details: {str(e)}"
        )