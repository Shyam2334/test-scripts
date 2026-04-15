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
    assert len(endpoints) > 0
    
    # Check that we have the expected endpoints
    paths = [ep["path"] for ep in endpoints]
    assert "/" in paths
    assert "/health" in paths
    assert "/api/v1/endpoints" in paths
    
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