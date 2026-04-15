from fastapi import FastAPI, status, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict
import os
from pathlib import Path

from app.api.endpoints_discovery import router as endpoints_router

app = FastAPI(
    title="Health Check Microservice",
    description="A simple FastAPI microservice with a health check endpoint.",
    version="0.1.0"
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the endpoints discovery router
app.include_router(endpoints_router)

@app.get("/", summary="Root endpoint", tags=["General"])
async def read_root() -> Dict[str, str]:
    """
    Returns a welcome message.
    """
    return {"message": "Welcome to the FastAPI Health Check Microservice!"}

@app.get(
    "/health",
    summary="Health Check",
    response_model=Dict[str, str],
    status_code=status.HTTP_200_OK,
    tags=["Monitoring"]
)
async def health_check() -> Dict[str, str]:
    """
    Performs a health check on the service.
    Returns a simple status indicating the service is operational.
    """
    return {"status": "ok"}

# Mount static files if they exist
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
    
    @app.get("/ui/{full_path:path}")
    async def serve_spa(full_path: str):
        """Serve the React SPA."""
        file_path = static_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(static_dir / "index.html")
    
    @app.get("/ui")
    async def serve_spa_root():
        """Serve the React SPA root."""
        return FileResponse(static_dir / "index.html")