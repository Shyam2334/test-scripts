import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_endpoints_discovery(client):
    """Test the endpoints discovery endpoint."""
    response = client.get("/api/v1/endpoints")
    assert response.status_code == 200
    
    endpoints = response.json()
    assert isinstance(endpoints, list)
    assert len(endpoints) == 2  # Health check and users endpoints should be visible
    
    # Check that we have both health and users endpoints
    paths = [ep["path"] for ep in endpoints]
    assert "/health" in paths
    assert "/api/users" in paths
    
    # Check endpoint structure
    for endpoint in endpoints:
        assert "path" in endpoint
        assert "methods" in endpoint
        assert "name" in endpoint
        assert "tags" in endpoint
        assert isinstance(endpoint["methods"], list)
        assert isinstance(endpoint["tags"], list)


def test_endpoints_sorted(client):
    """Test that endpoints are sorted by path."""
    response = client.get("/api/v1/endpoints")
    endpoints = response.json()
    
    paths = [ep["path"] for ep in endpoints]
    assert paths == sorted(paths)


def test_cors_headers(client):
    """Test that CORS headers are present."""
    response = client.get("/api/v1/endpoints", headers={"Origin": "http://localhost:3000"})
    assert response.status_code == 200
    assert "access-control-allow-origin" in response.headers


def test_only_health_endpoint_visible(client):
    """Test that only the allowed endpoints are visible in the discovery."""
    response = client.get("/api/v1/endpoints")
    endpoints = response.json()
    
    # Ensure only two endpoints are returned (health and users)
    assert len(endpoints) == 2
    
    # Get the paths
    paths = [ep["path"] for ep in endpoints]
    
    # Ensure we have health endpoint
    assert "/health" in paths
    health_endpoint = next(ep for ep in endpoints if ep["path"] == "/health")
    assert "GET" in health_endpoint["methods"]
    assert health_endpoint["name"] == "health_check"
    assert "Monitoring" in health_endpoint["tags"]
    
    # Ensure we have users endpoint
    assert "/api/users" in paths
    users_endpoint = next(ep for ep in endpoints if ep["path"] == "/api/users")
    assert "GET" in users_endpoint["methods"]
    assert users_endpoint["name"] == "get_users"
    assert "Users" in users_endpoint["tags"]


def test_hidden_endpoints_not_visible(client):
    """Test that other endpoints are not visible in the discovery."""
    response = client.get("/api/v1/endpoints")
    endpoints = response.json()
    
    paths = [ep["path"] for ep in endpoints]
    
    # These endpoints should NOT be visible
    assert "/" not in paths
    assert "/api/v1/endpoints" not in paths
    assert "/openapi.json" not in paths
    assert "/docs" not in paths
    assert "/redoc" not in paths