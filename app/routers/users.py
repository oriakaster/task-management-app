from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas
from ..authentication import create_access_token
from ..business import users as users_service

# Purpose: Router for user-related endpoints
router = APIRouter()

@router.post("/register", response_model=schemas.UserOut)
def register(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """input: UserCreate schema
       output: UserOut schema
       register a new user"""
    user = users_service.register_user(db, username=user_in.username, password=user_in.password)
    return user

@router.post("/login", response_model=schemas.Token)
def login(creds: schemas.LoginRequest, db: Session = Depends(get_db)):
    """input: LoginRequest schema
       output: Token schema
       authenticate a user and return a JWT token"""
    user = users_service.authenticate_user(db, username=creds.username, password=creds.password)
    token = create_access_token({"sub": user.username})
    return {"access_token": token, "token_type": "bearer"}
