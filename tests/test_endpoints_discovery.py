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
    assert len(endpoints) == 1  # Only health check endpoint should be visible
    
    # Check that we only have the health endpoint
    paths = [ep["path"] for ep in endpoints]
    assert paths == ["/health"]
    
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
    """Test that only the health check endpoint is visible in the discovery."""
    response = client.get("/api/v1/endpoints")
    endpoints = response.json()
    
    # Ensure only one endpoint is returned
    assert len(endpoints) == 1
    
    # Ensure it's the health endpoint
    health_endpoint = endpoints[0]
    assert health_endpoint["path"] == "/health"
    assert "GET" in health_endpoint["methods"]
    assert health_endpoint["name"] == "health_check"
    assert "Monitoring" in health_endpoint["tags"]


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