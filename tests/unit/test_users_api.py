import pytest
from fastapi.testclient import TestClient
from app.main import app


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


def test_get_users_endpoint_exists(client):
    """Test that the users endpoint exists and returns 200."""
    response = client.get("/api/users")
    assert response.status_code == 200


def test_get_users_returns_json(client):
    """Test that the users endpoint returns valid JSON."""
    response = client.get("/api/users")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_users_returns_10_users(client):
    """Test that the users endpoint returns exactly 10 users."""
    response = client.get("/api/users")
    data = response.json()
    assert len(data) == 10


def test_user_structure(client):
    """Test that each user has the correct structure."""
    response = client.get("/api/users")
    users = response.json()
    
    for user in users:
        assert "id" in user
        assert "name" in user
        assert "email" in user
        assert isinstance(user["id"], int)
        assert isinstance(user["name"], str)
        assert isinstance(user["email"], str)


def test_user_ids_are_unique(client):
    """Test that all user IDs are unique."""
    response = client.get("/api/users")
    users = response.json()
    
    ids = [user["id"] for user in users]
    assert len(ids) == len(set(ids))


def test_user_emails_are_valid(client):
    """Test that all user emails contain @ symbol."""
    response = client.get("/api/users")
    users = response.json()
    
    for user in users:
        assert "@" in user["email"]
        assert "." in user["email"]


def test_users_endpoint_in_discovery(client):
    """Test that the users endpoint appears in the endpoints discovery."""
    response = client.get("/api/v1/endpoints")
    endpoints = response.json()
    
    paths = [ep["path"] for ep in endpoints]
    assert "/api/users" in paths
    
    # Find the users endpoint
    users_endpoint = next(ep for ep in endpoints if ep["path"] == "/api/users")
    assert "GET" in users_endpoint["methods"]
    assert "Users" in users_endpoint["tags"]