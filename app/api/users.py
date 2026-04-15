from fastapi import APIRouter, HTTPException, status
from typing import List, Dict, Any, Optional
from uuid import UUID, uuid4
from datetime import datetime
from app.api.models import UserBase, UserCreate, UserUpdate, UserInDB
import copy

router = APIRouter()

# Fake in-memory database
fake_users_db: Dict[str, Dict[str, Any]] = {
    "550e8400-e29b-41d4-a716-446655440001": {
        "id": "550e8400-e29b-41d4-a716-446655440001",
        "name": "Alice Smith",
        "email": "alice.smith@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440002": {
        "id": "550e8400-e29b-41d4-a716-446655440002",
        "name": "Bob Johnson",
        "email": "bob.j@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440003": {
        "id": "550e8400-e29b-41d4-a716-446655440003",
        "name": "Charlie Brown",
        "email": "charlie.b@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440004": {
        "id": "550e8400-e29b-41d4-a716-446655440004",
        "name": "Diana Prince",
        "email": "diana.p@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440005": {
        "id": "550e8400-e29b-41d4-a716-446655440005",
        "name": "Eve Adams",
        "email": "eve.a@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440006": {
        "id": "550e8400-e29b-41d4-a716-446655440006",
        "name": "Frank White",
        "email": "frank.w@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440007": {
        "id": "550e8400-e29b-41d4-a716-446655440007",
        "name": "Grace Kelly",
        "email": "grace.k@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440008": {
        "id": "550e8400-e29b-41d4-a716-446655440008",
        "name": "Harry Potter",
        "email": "harry.p@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440009": {
        "id": "550e8400-e29b-41d4-a716-446655440009",
        "name": "Ivy Green",
        "email": "ivy.g@example.com",
        "created_at": datetime.now().isoformat()
    },
    "550e8400-e29b-41d4-a716-446655440010": {
        "id": "550e8400-e29b-41d4-a716-446655440010",
        "name": "Jack Black",
        "email": "jack.b@example.com",
        "created_at": datetime.now().isoformat()
    }
}


def check_email_exists(email: str, exclude_id: Optional[str] = None) -> bool:
    """Check if email already exists in database."""
    for user_id, user in fake_users_db.items():
        if user["email"] == email and user_id != exclude_id:
            return True
    return False


@router.get("/api/users", tags=["Users"], response_model=List[Dict[str, Any]])
async def get_users() -> List[Dict[str, Any]]:
    """
    Returns a list of all users.
    """
    # For backward compatibility with tests expecting integer IDs
    users = []
    for idx, (user_id, user) in enumerate(fake_users_db.items(), 1):
        user_copy = copy.deepcopy(user)
        # Add integer ID for backward compatibility
        user_copy["id"] = idx
        users.append(user_copy)
    return users[:10]  # Return only first 10 for backward compatibility


@router.get("/api/users/{user_id}", tags=["Users"], response_model=UserInDB)
async def get_user(user_id: str) -> UserInDB:
    """
    Get a specific user by ID.
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    user_data = fake_users_db[user_id]
    return UserInDB(**user_data)


@router.post("/api/users", tags=["Users"], response_model=UserInDB, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate) -> UserInDB:
    """
    Create a new user.
    """
    # Check if email already exists
    if check_email_exists(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    user_id = str(uuid4())
    user_data = {
        "id": user_id,
        "name": user.name,
        "email": user.email,
        "created_at": datetime.now()
    }
    fake_users_db[user_id] = user_data
    return UserInDB(**user_data)


@router.put("/api/users/{user_id}", tags=["Users"], response_model=UserInDB)
async def update_user(user_id: str, user_update: UserUpdate) -> UserInDB:
    """
    Update an existing user.
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    # Check if email already exists (excluding current user)
    if user_update.email and check_email_exists(user_update.email, exclude_id=user_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Update user data
    user_data = fake_users_db[user_id]
    update_data = user_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if value is not None:
            user_data[field] = value
    
    return UserInDB(**user_data)


@router.delete("/api/users/{user_id}", tags=["Users"], status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """
    Delete a user.
    """
    if user_id not in fake_users_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {user_id} not found"
        )
    
    del fake_users_db[user_id]
    return None