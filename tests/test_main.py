import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_read_root(client):
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the FastAPI Health Check Microservice!"}


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_openapi_schema(client):
    """Test that OpenAPI schema is accessible."""
    response = client.get("/openapi.json")
    assert response.status_code == 200
    assert "openapi" in response.json()
    assert response.json()["info"]["title"] == "Health Check Microservice"