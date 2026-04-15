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
    
    for route in app.routes:
        if isinstance(route, APIRoute):
            # Filter out internal routes
            if not any(skip in route.path for skip in ["/openapi.json", "/docs", "/redoc"]):
                endpoints.append({
                    "path": route.path,
                    "methods": list(route.methods),
                    "name": route.name,
                    "tags": route.tags if route.tags else []
                })
    
    return sorted(endpoints, key=lambda x: x["path"])