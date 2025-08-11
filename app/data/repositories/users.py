from sqlalchemy.orm import Session
from .. import models
from ...core.errors import UserNotFoundError, UsernameTakenError
from sqlalchemy.exc import SQLAlchemyError
from ...core.errors import DatabaseError

def find_by_username(db: Session, username: str) -> models.User | None:
    """Safe finder for login/duplicate checks: returns user or None (no exceptions)."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_by_username(db: Session, username: str) -> models.User:
    """Strict getter: raise 404 if the user doesn't exist."""
    user = find_by_username(db, username)
    if not user:
        raise UserNotFoundError(username)
    return user

def create_user(db: Session, *, username: str, password_hash: str) -> models.User:
    """Create a user; raise 400 if the username is already taken."""
    if find_by_username(db, username):  # <-- use the safe finder here
        raise UsernameTakenError(username)
    user = models.User(username=username, password_hash=password_hash)
    try:
        db.add(user); db.commit(); db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        # Bubble as a domain error; handler will return 500 JSON
        raise DatabaseError() from e

def get_by_id(db: Session, user_id: int) -> models.User:
    """Get user by ID; raise 404 if not found."""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"id:{user_id}")
    return user
