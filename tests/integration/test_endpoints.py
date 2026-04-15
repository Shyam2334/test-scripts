"""Integration tests for API endpoints."""
import pytest
from fastapi.testclient import TestClient
from app.main import app
import logging


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    with TestClient(app) as test_client:
        yield test_client


def test_root_endpoint_logging(client, caplog):
    """Test that root endpoint logs access."""
    with caplog.at_level(logging.INFO):
        response = client.get("/")
        assert response.status_code == 200
        assert "Root endpoint accessed" in caplog.text


def test_health_endpoint_logging(client, caplog):
    """Test that health endpoint logs access."""
    with caplog.at_level(logging.INFO):
        response = client.get("/health")
        assert response.status_code == 200
        assert "Health check endpoint accessed" in caplog.text


def test_startup_shutdown_events(caplog):
    """Test application startup and shutdown logging."""
    with caplog.at_level(logging.INFO):
        with TestClient(app):
            assert "Starting up FastAPI Health Check Microservice" in caplog.text
        assert "Shutting down FastAPI Health Check Microservice" in caplog.text


def test_invalid_endpoint(client):
    """Test accessing an invalid endpoint."""
    response = client.get("/invalid")
    assert response.status_code == 404
    assert "detail" in response.json()