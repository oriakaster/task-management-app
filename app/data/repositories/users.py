from sqlalchemy.orm import Session
from .. import models
from ...core.errors import UserNotFoundError, UsernameTakenError
from sqlalchemy.exc import SQLAlchemyError
from ...core.errors import DatabaseError

def find_by_username(db: Session, username: str) -> models.User | None:
    """input: username; 
       output: User or None(if the user doesn't exist).
       find the user by username."""
    return db.query(models.User).filter(models.User.username == username).first()

def get_by_username(db: Session, username: str) -> models.User:
    """input: username; 
       output: User;
       get the user by username;"""
    user = find_by_username(db, username)
    if not user:
        raise UserNotFoundError(username)
    return user

def create_user(db: Session, *, username: str, password_hash: str) -> models.User:
    """input: username, password_hash;
       output: User;
       create a new user with the given username and password hash."""
    if find_by_username(db, username):  
        raise UsernameTakenError(username)
    user = models.User(username=username, password_hash=password_hash)
    try:
        db.add(user); db.commit(); db.refresh(user)
        return user
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError() from e

def get_by_id(db: Session, user_id: int) -> models.User:
    """input: user_id;
       output: User;
       get the user by user_id;"""
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"id:{user_id}")
    return user
