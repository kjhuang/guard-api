"""
jwt auth
"""

from datetime import datetime, timedelta, timezone
from typing import Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import (
    APIKeyHeader,
    HTTPAuthorizationCredentials,
    HTTPBearer,
    OAuth2PasswordBearer,
)
from jose import JWTError, jwt

# Secret key and algorithm for JWT
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_DAYS = 180

API_KEY_NAME = "WIS-API-KEY"
API_KEYS = ["123456"]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

http_bearer = HTTPBearer(auto_error=False)

api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Generate a JWT token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_token(token: str):
    """Verify the JWT token and return the decoded data."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Returns the decoded payload
    except JWTError:
        return None


def verify_jwt_token(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(http_bearer),
):
    """
    Optionally validate a JWT token if the Authorization header is present.
    """
    if not credentials:
        return None  # No Authorization header provided
    try:
        token = credentials.credentials
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # Return decoded payload if valid
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid JWT token",
        )


def verify_api_key(api_key: Optional[str] = Depends(api_key_header)):
    """
    Optionally validate an API key if the WIS-API-KEY header is present.
    """
    if not api_key:
        return None  # No API key provided
    # Replace with your actual API key validation logic
    if api_key not in API_KEYS:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API Key",
        )
    return api_key  # Return the API key if valid


def authenticate(
    jwt_payload: Optional[dict] = Depends(verify_jwt_token),
    api_key: Optional[str] = Depends(verify_api_key),
):
    """
    Authenticate using either JWT or API Key.
    """
    # Check if a valid JWT payload exists
    if jwt_payload:
        return {"auth_type": "jwt", "payload": jwt_payload}

    # Check if a valid API key exists
    if api_key:
        return {"auth_type": "api_key", "key": api_key}

    # If neither is valid
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Authorization credentials missing or invalid",
    )
