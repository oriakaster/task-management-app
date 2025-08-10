# app/core/errors.py
from dataclasses import dataclass

@dataclass
class AppError(Exception):
    code: str
    message: str
    http_status: int = 400

# Auth / Users
class UserNotFoundError(AppError):
    def __init__(self, username: str):
        super().__init__("USER_NOT_FOUND", f"User '{username}' not found", 404)

class UsernameTakenError(AppError):
    def __init__(self, username: str):
        super().__init__("USERNAME_TAKEN", f"Username '{username}' already taken", 409)

class InvalidCredentialsError(AppError):
    def __init__(self):
        super().__init__("INVALID_CREDENTIALS", "Invalid username or password", 401)

# Tasks
class TaskNotFoundError(AppError):
    def __init__(self, task_id: int):
        super().__init__("TASK_NOT_FOUND", f"Task {task_id} not found", 404)

class TaskForbiddenError(AppError):
    def __init__(self):
        super().__init__("TASK_FORBIDDEN", "You are not allowed to access this task", 403)

# Infra / DB
class DatabaseError(AppError):
    def __init__(self, msg: str = "Database error"):
        super().__init__("DATABASE_ERROR", msg, 500)
