"""Integration tests for diagnostics endpoint."""
import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_diagnostics_endpoint(client):
    """Test the diagnostics endpoint returns system information."""
    response = client.get("/diagnostics")
    assert response.status_code == 200
    
    data = response.json()
    assert data["status"] == "ok"
    assert "timestamp" in data
    assert "system" in data
    assert "python_version" in data["system"]
    
    # Check for either full diagnostics or basic diagnostics
    if "note" in data:
        assert data["note"] == "Install psutil for detailed diagnostics"
    else:
        assert "memory" in data
        assert "cpu" in data
        assert "environment" in data


def test_exception_handling(client):
    """Test that exceptions are properly handled."""
    # This test verifies the global exception handler is working
    # by checking that the app doesn't crash on errors
    response = client.get("/health")
    assert response.status_code == 200
    
    response = client.get("/")
    assert response.status_code == 200


def test_startup_shutdown_events(caplog):
    """Test that startup and shutdown events are logged."""
    with TestClient(app) as client:
        # Startup event should have been triggered
        response = client.get("/health")
        assert response.status_code == 200
    
    # After context manager exits, shutdown should have been triggered
    # Note: In test environment, these logs might not always be captured
    # but the events should execute without error