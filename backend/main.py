from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from config import settings
from database import connect_to_mongodb, close_mongodb_connection, ping_database
from routers import auth, onboarding, stages, milestones, progress, resources, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for startup and shutdown events.
    Handles MongoDB connection lifecycle.
    """
    # Startup: Connect to MongoDB
    await connect_to_mongodb()
    yield
    # Shutdown: Close MongoDB connection
    await close_mongodb_connection()


# Initialize FastAPI application
app = FastAPI(
    title="Pathways for Parents API",
    description="Backend API for Pathways for Parents platform",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

# Register routers
app.include_router(auth.router, prefix="/api/v1")
app.include_router(users.router)
app.include_router(onboarding.router)
app.include_router(stages.router)
app.include_router(milestones.router)
app.include_router(progress.router)
app.include_router(resources.router)


@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "name": "Pathways for Parents API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/healthz")
async def health_check():
    """
    Health check endpoint with database connectivity verification.
    Returns the health status of the API and database connection.
    """
    db_connected = await ping_database()
    
    if db_connected:
        return {
            "status": "ok",
            "database": "connected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    else:
        return {
            "status": "degraded",
            "database": "disconnected",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=settings.app_env == "development"
    )