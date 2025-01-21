from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from crud import crud_tenant

router = APIRouter(prefix="/dashboard")
templates = Jinja2Templates(directory="app/templates")


@router.get("/tenants", name="tenants")
async def tenants_page(
        request: Request,
        db: AsyncSession = Depends(get_db)
):
    tenants = await crud_tenant.get_multi(db=db)
    return templates.TemplateResponse(
        "tenants.html",
        {
            "request": request,
            "tenants": tenants,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }
    )


@router.get("/tenants/{tenant_id}", name="tenant_details")
async def tenant_details(
        request: Request,
        tenant_id: int,
        db: AsyncSession = Depends(get_db)
):
    try:
        # Await the tenant data before passing to template
        tenant = await crud_tenant.get(db=db, id=tenant_id)

        if not tenant:
            raise HTTPException(status_code=404, detail="Tenant not found")

        # Get additional data if needed
        # maintenance_history = await crud_tenant.maintenance.get_tenant_history(db=db, tenant_id=tenant_id)

        # Calculate financial summary
        # total_funds = await crud_tenant.fund.get_tenant_total(db=db, tenant_id=tenant_id)
        # total_costs = await crud_tenant.cost.get_tenant_total(db=db, tenant_id=tenant_id)

        # Prepare the context with all required data
        context = {
            "request": request,  # Required by Starlette
            "tenant": tenant,
            # "maintenance_history": maintenance_history[:3] if maintenance_history else [],
            # "total_funds": total_funds,
            # "total_costs": total_costs,
            "current_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        return templates.TemplateResponse(
            "tenant_detail.html",
            context
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving tenant details: {str(e)}"
        )