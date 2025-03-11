from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..models.auth import Token, UserCreate, User
from ..utils.auth import (
    verify_password,
    create_access_token,
    get_current_active_user,
    get_password_hash
)
from ...core.database import get_db
from ...repositories import UserRepository
from ...config import settings

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    user = user_repository.get_by_username(username=form_data.username)
    if not user or not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Update last login time
    user_repository.update(user.id, {"last_login": "CURRENT_TIMESTAMP"})
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/register", response_model=User)
async def register_user(user: UserCreate, db: Session = Depends(get_db)):
    user_repository = UserRepository(db)
    
    # Check if username exists
    if user_repository.get_by_username(username=user.username):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if user_repository.get_by_email(email=user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user.password)
    db_user = user_repository.create({
        "username": user.username,
        "email": user.email,
        "password": hashed_password,
        "role": "user",
        "status": "active"
    })
    
    return db_user

@router.get("/me", response_model=User)
async def read_users_me(current_user = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=User)
async def update_user_me(
    user_update: UserCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    user_repository = UserRepository(db)
    
    # Check if username is taken by another user
    if (user_update.username != current_user.username and 
        user_repository.get_by_username(username=user_update.username)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email is taken by another user
    if (user_update.email != current_user.email and 
        user_repository.get_by_email(email=user_update.email)):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Update user
    update_data = {
        "username": user_update.username,
        "email": user_update.email
    }
    
    if user_update.password:
        update_data["password"] = get_password_hash(user_update.password)
    
    updated_user = user_repository.update(current_user.id, update_data)
    return updated_user