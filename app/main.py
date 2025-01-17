from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.templating import Jinja2Templates
from core.config import settings
from app.api.v1 import (
    buildings,
    # floors,
    units,
    # owners,
    # tenants,
    # funds,
    # transactions,
    charges,
    # costs,
)
from app.front_page.routers import (
    dashboard as front_page_dashboard,
    buildings as front_page_buildings,
    home as front_page_home,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    description="Building Management System API"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add error handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={"detail": exc.errors()}
    )

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Templates
templates = Jinja2Templates(directory="app/templates")

# Include routers
app.include_router(buildings.router, prefix=settings.API_V1_STR, tags=["buildings"])
# app.include_router(floors.router, prefix=settings.API_V1_STR, tags=["floors"])
app.include_router(units.router, prefix=settings.API_V1_STR, tags=["units"])
# app.include_router(owners.router, prefix=settings.API_V1_STR, tags=["owners"])
# app.include_router(tenants.router, prefix=settings.API_V1_STR, tags=["tenants"])
# app.include_router(funds.router, prefix=settings.API_V1_STR, tags=["funds"])
# app.include_router(transactions.router, prefix=settings.API_V1_STR, tags=["transactions"])
app.include_router(front_page_dashboard.router, prefix="", tags=["dashboards"])
app.include_router(front_page_buildings.router, prefix="", tags=["dashboards"])
app.include_router(front_page_home.router, prefix="", tags=["dashboards"])


# Add health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}