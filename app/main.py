from fastapi import FastAPI, status, Request
from fastapi.responses import JSONResponse
from typing import Dict, Any
import logging
import sys
import traceback
from datetime import datetime
import os
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown."""
    # Startup
    logger.info("Application starting up")
    logger.info(f"Python version: {sys.version}")
    try:
        import fastapi
        logger.info(f"FastAPI version: {fastapi.__version__}")
    except AttributeError:
        logger.info("FastAPI version information not available")
    
    yield
    
    # Shutdown
    logger.info("Application shutting down")


app = FastAPI(
    title="Health Check Microservice",
    description="A simple FastAPI microservice with a health check endpoint.",
    version="0.1.0",
    lifespan=lifespan
)

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle all unhandled exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "type": type(exc).__name__,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

@app.get("/", summary="Root endpoint", tags=["General"])
async def read_root() -> Dict[str, str]:
    """
    Returns a welcome message.
    """
    try:
        logger.info("Root endpoint accessed")
        return {"message": "Welcome to the FastAPI Health Check Microservice!"}
    except Exception as e:
        logger.error(f"Error in root endpoint: {e}", exc_info=True)
        raise

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
    try:
        logger.info("Health check endpoint accessed")
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error in health check: {e}", exc_info=True)
        raise

@app.get(
    "/diagnostics",
    summary="System Diagnostics",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
    tags=["Monitoring"]
)
async def diagnostics() -> Dict[str, Any]:
    """
    Provides detailed system diagnostics for troubleshooting.
    """
    try:
        import platform
        import psutil
        
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "platform": platform.system(),
                "platform_release": platform.release(),
                "platform_version": platform.version(),
                "architecture": platform.machine(),
                "processor": platform.processor(),
                "python_version": sys.version,
            },
            "memory": {
                "total": psutil.virtual_memory().total,
                "available": psutil.virtual_memory().available,
                "percent": psutil.virtual_memory().percent,
                "used": psutil.virtual_memory().used,
            },
            "cpu": {
                "count": psutil.cpu_count(),
                "percent": psutil.cpu_percent(interval=1),
            },
            "environment": {
                "debug_mode": os.getenv("DEBUG", "false").lower() == "true",
                "log_level": logging.getLevelName(logger.level),
            }
        }
    except ImportError:
        logger.warning("psutil not installed, returning basic diagnostics")
        return {
            "status": "ok",
            "timestamp": datetime.utcnow().isoformat(),
            "system": {
                "platform": platform.system() if 'platform' in locals() else "unknown",
                "python_version": sys.version,
            },
            "note": "Install psutil for detailed diagnostics"
        }
    except Exception as e:
        logger.error(f"Error in diagnostics: {e}", exc_info=True)
        raise