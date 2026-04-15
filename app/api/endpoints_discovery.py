from fastapi import APIRouter, Request
from typing import List, Dict, Any
from fastapi.routing import APIRoute

router = APIRouter()


@router.get("/api/v1/endpoints", tags=["Discovery"])
async def list_endpoints(request: Request) -> List[Dict[str, Any]]:
    """
    Returns a JSON list of all registered API endpoints.
    """
    app = request.app
    endpoints = []
    
    # Only include the health check endpoint and users endpoint
    allowed_paths = ["/health", "/api/users"]
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            # Only include explicitly allowed routes
            if route.path in allowed_paths:
                # For /api/users, only include GET method
                if route.path == "/api/users" and "GET" not in route.methods:
                    continue
                    
                endpoints.append({
                    "path": route.path,
                    "methods": list(route.methods),
                    "name": route.name,
                    "tags": route.tags if route.tags else []
                })
    
    return sorted(endpoints, key=lambda x: x["path"])