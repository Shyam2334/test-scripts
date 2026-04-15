import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.api.users import fake_users_db
import copy


@pytest.fixture
def client():
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_db():
    """Reset the fake database before each test."""
    # Store original state
    original_db = copy.deepcopy(fake_users_db)
    yield
    # Restore original state
    fake_users_db.clear()
    fake_users_db.update(original_db)


def test_full_user_crud_flow(client):
    """Test the complete CRUD flow for a user."""
    # Step 1: Create a user
    user_data = {
        "name": "Integration Test User",
        "email": "integration@test.com"
    }
    create_response = client.post("/api/users", json=user_data)
    assert create_response.status_code == 201
    
    created_user = create_response.json()
    user_id = created_user["id"]
    assert created_user["name"] == user_data["name"]
    assert created_user["email"] == user_data["email"]
    
    # Step 2: Get the created user
    get_response = client.get(f"/api/users/{user_id}")
    assert get_response.status_code == 200
    
    fetched_user = get_response.json()
    assert fetched_user["id"] == user_id
    assert fetched_user["name"] == user_data["name"]
    assert fetched_user["email"] == user_data["email"]
    
    # Step 3: Update the user
    update_data = {
        "name": "Updated Integration User",
        "email": "updated.integration@test.com"
    }
    update_response = client.put(f"/api/users/{user_id}", json=update_data)
    assert update_response.status_code == 200
    
    updated_user = update_response.json()
    assert updated_user["id"] == user_id
    assert updated_user["name"] == update_data["name"]
    assert updated_user["email"] == update_data["email"]
    
    # Step 4: Get the updated user to verify changes
    verify_response = client.get(f"/api/users/{user_id}")
    assert verify_response.status_code == 200
    
    verified_user = verify_response.json()
    assert verified_user["name"] == update_data["name"]
    assert verified_user["email"] == update_data["email"]
    
    # Step 5: Delete the user
    delete_response = client.delete(f"/api/users/{user_id}")
    assert delete_response.status_code == 204
    
    # Step 6: Attempt to get the deleted user (should fail)
    final_response = client.get(f"/api/users/{user_id}")
    assert final_response.status_code == 404
    assert "not found" in final_response.json()["detail"]


def test_multiple_users_crud(client):
    """Test CRUD operations with multiple users."""
    # Create multiple users
    users_data = [
        {"name": "User One", "email": "user1@integration.com"},
        {"name": "User Two", "email": "user2@integration.com"},
        {"name": "User Three", "email": "user3@integration.com"}
    ]
    
    created_users = []
    for user_data in users_data:
        response = client.post("/api/users", json=user_data)
        assert response.status_code == 201
        created_users.append(response.json())
    
    # Verify all users were created
    for i, created_user in enumerate(created_users):
        response = client.get(f"/api/users/{created_user['id']}")
        assert response.status_code == 200
        assert response.json()["name"] == users_data[i]["name"]
        assert response.json()["email"] == users_data[i]["email"]
    
    # Update the second user
    user2_id = created_users[1]["id"]
    update_data = {"name": "User Two Updated"}
    response = client.put(f"/api/users/{user2_id}", json=update_data)
    assert response.status_code == 200
    assert response.json()["name"] == "User Two Updated"
    
    # Delete the first user
    user1_id = created_users[0]["id"]
    response = client.delete(f"/api/users/{user1_id}")
    assert response.status_code == 204
    
    # Verify first user is deleted
    response = client.get(f"/api/users/{user1_id}")
    assert response.status_code == 404
    
    # Verify other users still exist
    response = client.get(f"/api/users/{created_users[1]['id']}")
    assert response.status_code == 200
    
    response = client.get(f"/api/users/{created_users[2]['id']}")
    assert response.status_code == 200


def test_error_handling_flow(client):
    """Test error handling in CRUD operations."""
    # Try to get non-existent user
    fake_id = "550e8400-e29b-41d4-a716-446655440000"
    response = client.get(f"/api/users/{fake_id}")
    assert response.status_code == 404
    
    # Try to create user with invalid data
    invalid_data = {"name": ""}  # Missing email, empty name
    response = client.post("/api/users", json=invalid_data)
    assert response.status_code == 422
    
    # Create a user
    user_data = {"name": "Error Test User", "email": "error@test.com"}
    create_response = client.post("/api/users", json=user_data)
    assert create_response.status_code == 201
    
    # Try to create another user with same email
    duplicate_data = {"name": "Duplicate User", "email": "error@test.com"}
    response = client.post("/api/users", json=duplicate_data)
    assert response.status_code == 400
    
    # Try to update non-existent user
    response = client.put(f"/api/users/{fake_id}", json={"name": "Updated"})
    assert response.status_code == 404
    
    # Try to delete non-existent user
    response = client.delete(f"/api/users/{fake_id}")
    assert response.status_code == 404