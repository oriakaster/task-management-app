import logging
from typing import Optional
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..core.errors import UsernameTakenError, InvalidCredentialsError
from ..authentication import hash_password, verify_password
from ..data.repositories import users as users_repo
from ..data import models

logger = logging.getLogger(__name__)

def register_user(db: Session, *, username: str, password: str) -> models.User:
    """Idempotent registration.
    - If the user doesn't exist -> create and return (200).
    - If the user exists and password matches -> return existing (200).
    - If the user exists and password doesn't match -> 409 Conflict.
    """
    existing = users_repo.find_by_username(db, username)
    if existing:
        if verify_password(password, existing.password_hash):
            logger.info("User %s already exists, returning existing user", username)
            return existing
        logger.warning("Username %s already taken with a different password", username)
        raise UsernameTakenError(username)

    pwd_hash = hash_password(password)
    user = users_repo.create_user(db, username=username, password_hash=pwd_hash)
    logger.info("User %s registered successfully", username)
    return user

def authenticate_user(db: Session, *, username: str, password: str) -> Optional[models.User]:
    user = users_repo.find_by_username(db, username)
    if not user or not verify_password(password, user.password_hash):
        logger.warning("Authentication failed for user %s", username)
        raise InvalidCredentialsError()  
    logger.info("User %s authenticated successfully", username)
    return user
