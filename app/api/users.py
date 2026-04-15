from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

# Mock user data
MOCK_USERS = [
    {"id": 1, "name": "Alice Smith", "email": "alice.smith@example.com"},
    {"id": 2, "name": "Bob Johnson", "email": "bob.j@example.com"},
    {"id": 3, "name": "Charlie Brown", "email": "charlie.b@example.com"},
    {"id": 4, "name": "Diana Prince", "email": "diana.p@example.com"},
    {"id": 5, "name": "Eve Adams", "email": "eve.a@example.com"},
    {"id": 6, "name": "Frank White", "email": "frank.w@example.com"},
    {"id": 7, "name": "Grace Kelly", "email": "grace.k@example.com"},
    {"id": 8, "name": "Harry Potter", "email": "harry.p@example.com"},
    {"id": 9, "name": "Ivy Green", "email": "ivy.g@example.com"},
    {"id": 10, "name": "Jack Black", "email": "jack.b@example.com"},
]

@router.get("/api/users", tags=["Users"], response_model=List[Dict[str, Any]])
async def get_users() -> List[Dict[str, Any]]:
    """
    Returns a list of 10 mock users.
    """
    return MOCK_USERS