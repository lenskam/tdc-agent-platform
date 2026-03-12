from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from .jwt_handler import verify_token


security = HTTPBearer()


class CurrentUser:
    def __init__(self, user_id: str, email: str, role: str, username: str):
        self.user_id = user_id
        self.email = email
        self.role = role
        self.username = username


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Extract and validate the current user from JWT token.
    
    Args:
        credentials: HTTP Authorization credentials
        
    Returns:
        CurrentUser object with user data
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials
    
    payload = verify_token(token, "access")
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user_id = payload.get("sub")
    email = payload.get("email")
    role = payload.get("role", "user")
    username = payload.get("username", email)
    
    if not user_id or not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return CurrentUser(
        user_id=user_id,
        email=email,
        role=role,
        username=username
    )


async def get_current_active_user(
    current_user: CurrentUser = Depends(get_current_user)
) -> CurrentUser:
    """
    Verify that the current user is active.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        CurrentUser if active
        
    Raises:
        HTTPException: If user is inactive
    """
    # In a real app, you'd check the database for is_active status
    # For now, we assume all users from valid tokens are active
    return current_user


def require_role(*allowed_roles: str):
    """
    Dependency factory for role-based access control.
    
    Args:
        *allowed_roles: Roles that are allowed to access the endpoint
        
    Returns:
        Dependency that checks user role
    """
    async def role_checker(current_user: CurrentUser = Depends(get_current_user)) -> CurrentUser:
        if current_user.role not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Access denied. Required roles: {', '.join(allowed_roles)}"
            )
        return current_user
    
    return role_checker


require_admin = require_role("admin")
require_manager = require_role("admin", "manager")
