from fastapi import APIRouter
from .v1 import api_router as v1_router
from .v2 import api_router as v2_router

# Main API router for all versions
main_api_router = APIRouter()

# Include versioned routers
main_api_router.include_router(v1_router, prefix="/v1")
main_api_router.include_router(v2_router, prefix="/v2")