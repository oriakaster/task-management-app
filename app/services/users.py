from typing import Optional
from sqlalchemy.orm import Session
from ..authentication import hash_password, verify_password
from ..data.repositories import users as users_repo
from ..data import models

def register_user(db: Session, *, username: str, password: str) -> models.User:
    pwd_hash = hash_password(password)
    return users_repo.create_user(db, username=username, password_hash=pwd_hash)

def authenticate_user(db: Session, *, username: str, password: str) -> Optional[models.User]:
    user = users_repo.find_by_username(db, username)  # <-- safe finder
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user
