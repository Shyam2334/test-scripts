from fastapi import FastAPI, status
from typing import Dict
import logging
from contextlib import asynccontextmanager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    # Startup
    logger.info("Starting up FastAPI Health Check Microservice")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI Health Check Microservice")


app = FastAPI(
    title="Health Check Microservice",
    description="A simple FastAPI microservice with a health check endpoint.",
    version="0.1.0",
    lifespan=lifespan
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
        logger.error(f"Error in root endpoint: {str(e)}")
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
        # Add actual health checks here if needed
        # For example: database connectivity, external service availability, etc.
        return {"status": "ok"}
    except Exception as e:
        logger.error(f"Error in health check: {str(e)}")
        return {"status": "error"}