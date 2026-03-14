from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session

from ...database.postgres import get_db
from ...database.models import User
from ...auth.jwt_handler import create_access_token, create_refresh_token
from ...auth.password import hash_password, verify_password


router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str
    full_name: Optional[str] = None
    role: str = "user"


class UserLogin(BaseModel):
    email: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    user: dict


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: Optional[str]
    role: str
    is_active: bool

    class Config:
        from_attributes = True


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """
    Register a new user.
    """
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User with this email or username already exists"
        )
    
    hashed_pwd, salt = hash_password(user_data.password)
    
    new_user = User(
        email=user_data.email,
        username=user_data.username,
        hashed_password=hashed_pwd,
        full_name=user_data.full_name,
        role=user_data.role,
        is_active=1
    )
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return UserResponse(
        id=new_user.id,
        email=new_user.email,
        username=new_user.username,
        full_name=new_user.full_name,
        role=new_user.role,
        is_active=bool(new_user.is_active)
    )


@router.post("/login", response_model=TokenResponse)
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authenticate user and return JWT tokens.
    """
    user = db.query(User).filter(User.email == credentials.email).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password, ""):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    access_token = create_access_token({
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role
    })
    
    refresh_token = create_refresh_token({
        "sub": str(user.id),
        "email": user.email,
        "username": user.username,
        "role": user.role
    })
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "userId": str(user.id),
            "email": user.email,
            "username": user.username,
            "role": user.role
        }
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(db: Session = Depends(get_db), current_user_id: int = Depends(lambda: 1)):
    """
    Get current authenticated user info.
    """
    user = db.query(User).filter(User.id == current_user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(
        id=user.id,
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        role=user.role,
        is_active=bool(user.is_active)
    )


DEMO_USERS = {
    "admin@tdc.com": {"password": "admin123", "user_id": "1", "role": "admin"},
}


@router.post("/login-demo", response_model=TokenResponse)
async def login_demo():
    """
    Demo login for testing without database.
    """
    access_token = create_access_token({
        "sub": "1",
        "email": "admin@tdc.com",
        "username": "admin",
        "role": "admin"
    })
    
    refresh_token = create_refresh_token({
        "sub": "1",
        "email": "admin@tdc.com",
        "username": "admin",
        "role": "admin"
    })
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        user={
            "userId": "1",
            "email": "admin@tdc.com",
            "username": "admin",
            "role": "admin"
        }
    )
