from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models

def find_by_username(db: Session, username: str) -> models.User | None:
    """Safe finder for login/duplicate checks: returns user or None (no exceptions)."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_by_username(db: Session, username: str) -> models.User:
    """Strict getter: raise 404 if the user doesn't exist."""
    user = find_by_username(db, username)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

def create_user(db: Session, *, username: str, password_hash: str) -> models.User:
    """Create a user; raise 400 if the username is already taken."""
    if find_by_username(db, username):  # <-- use the safe finder here
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already taken")
    user = models.User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def get_by_id(db: Session, user_id: int) -> models.User:
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user
