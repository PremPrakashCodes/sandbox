from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.core.redis import redis_connection
from app.api.v1 import api_router as v1_router
from app.api.v2 import api_router as v2_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await redis_connection.connect()
    yield
    # Shutdown
    await redis_connection.disconnect()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    debug=settings.debug,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers with versioning
app.include_router(v1_router, prefix="/api/v1")
app.include_router(v2_router, prefix="/api/v2")