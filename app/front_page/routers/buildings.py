from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException
from fastapi import Request
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_db
from app.schemas.building import BuildingResponse
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


async def building_detail(
        building_id: int,
        db: AsyncSession = Depends(get_db)
) -> BuildingResponse:
    try:
        # Get the building from database
        building = await crud_building.get(db=db, id=building_id)

        if not building:
            raise HTTPException(
                status_code=404,
                detail="Building not found"
            )

        # Get additional building statistics
        # Calculate occupancy rate and other metrics
        building_response = BuildingResponse(
            id=building.id,
            name=building.name,
            total_floors=building.total_floors,
            description=building.description,
            created_at=building.created_at,
            updated_at=building.updated_at,
            is_deleted=building.is_deleted,
            deleted_at=building.deleted_at,
        )

        # Additional calculations could be added here
        # For example:
        # - Calculate occupancy rate
        # - Get total units
        # - Get maintenance history
        # - Get financial summary

        # Get relationships data
        floors = building.floors
        funds = building.funds
        charges = building.charges
        costs = building.costs

        # Add summary data
        total_units = sum(len(floor.units) for floor in floors) if floors else 0
        total_costs = sum(cost.amount for cost in costs) if costs else 0
        total_charges = sum(charge.amount for charge in charges) if charges else 0
        total_funds = sum(fund.amount for fund in funds) if funds else 0

        # Add these calculated fields to the response
        building_response.total_units = total_units
        building_response.total_costs = total_costs
        building_response.total_charges = total_charges
        building_response.total_funds = total_funds
        building_response.net_balance = total_funds - total_costs

        # Calculate the building age
        if building.created_at:
            current_time = datetime.now(timezone.utc)
            building_age = (current_time - building.created_at).days
            building_response.age_in_days = building_age

        return building_response

    except Exception as e:
        # Log the error here
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while retrieving building details: {str(e)}"
        )


@router.get("/buildings/{building_id}", name="building_details")
async def building_details(
        request: Request,
        building_id: int,
        db: AsyncSession = Depends(get_db)
):
    # Fetch and return building details
    return templates.TemplateResponse(
        "building_detail.html",
        {
            "request": request,
            "building": building_detail(building_id=building_id, db=db)
        }
    )
