from fastapi import FastAPI, status
from typing import Dict

app = FastAPI(
    title="Health Check Microservice",
    description="A simple FastAPI microservice with a health check endpoint.",
    version="0.1.0"
)

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