# app/core/errors.py
from dataclasses import dataclass
from typing import Any, Dict, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class AppError(Exception):
    """Base exception for all application errors"""
    code: str
    message: str
    http_status: int = 400
    details: Optional[Dict[str, Any]] = None
    
# Auth / Users
class UserNotFoundError(AppError):
    def __init__(self, username: str):
        """input: username (str)
           output: UserNotFoundError with message and HTTP status 404
           Raise when a user is not found in the database"""
        super().__init__("USER_NOT_FOUND", f"User '{username}' not found", 404)

class UsernameTakenError(AppError):
    def __init__(self, username: str):
        """input: username (str)
           output: UsernameTakenError with message and HTTP status 409
           Raise when trying to register a user with an already taken username"""
        super().__init__("USERNAME_TAKEN", f"Username '{username}' already taken", 409)

class InvalidCredentialsError(AppError):
    def __init__(self):
        """input: None
           output: InvalidCredentialsError with message and HTTP status 401
           Raise when authentication fails due to invalid username or password"""
        super().__init__("INVALID_CREDENTIALS", "Invalid username or password", 401)
        
class InvalidPasswordError(AppError):
    def __init__(self):
        """input: None
           output: InvalidPasswordError with message and HTTP status 401
           Raise when the provided password is incorrect during authentication"""
        super().__init__("INVALID_PASSWORD", "Password is incorrect", 401)

# Tasks
class TaskNotFoundError(AppError):
    def __init__(self, task_id: int):
        """input: task_id (int)
           output: TaskNotFoundError with message and HTTP status 404
           Raise when a task is not found for the current user"""
        super().__init__("TASK_NOT_FOUND", f"Task {task_id} not found", 404)

class TaskForbiddenError(AppError):
    def __init__(self):
        """input: None
           output: TaskForbiddenError with message and HTTP status 403
           Raise when trying to access a task that does not belong to the current user"""
        super().__init__("TASK_FORBIDDEN", "You are not allowed to access this task", 403)

# DB
class DatabaseError(AppError):
    def __init__(self, msg: str = "Database error"):
        """input: msg (str)
           output: DatabaseError with message and HTTP status 500
           Raise when there is a general database error"""
        super().__init__("DATABASE_ERROR", msg, 500)
