"""
auth route
"""

from datetime import timedelta

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.auth.auth_handler import create_access_token

router = APIRouter(prefix="/api/auth", tags=["auth"])


class User(BaseModel):
    username: str
    password: str


fake_users_db = {"user1": {"username": "user1", "password": "password1"}}


@router.post("/token")
def login(user: User):
    """Login endpoint to issue a JWT."""
    if (
        user.username in fake_users_db
        and user.password == fake_users_db[user.username]["password"]
    ):
        access_token = create_access_token(
            data={"sub": user.username}, expires_delta=timedelta(minutes=30)
        )
        return {"access_token": access_token, "token_type": "bearer"}
    else:
        raise HTTPException(status_code=400, detail="Invalid username or password")
