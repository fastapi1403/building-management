from fastapi import APIRouter
from src.api.v1.endpoints import buildings, units, charges, transactions, reports

api_router = APIRouter()
api_router.include_router(buildings.router, prefix="/buildings", tags=["buildings"])
api_router.include_router(units.router, prefix="/units", tags=["units"])
api_router.include_router(charges.router, prefix="/charges", tags=["charges"])
api_router.include_router(transactions.router, prefix="/transactions", tags=["transactions"])
api_router.include_router(reports.router, prefix="/reports", tags=["reports"])
