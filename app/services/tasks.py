import logging
from sqlalchemy.orm import Session
from ..data import models
from ..data.repositories import tasks as tasks_crud

logger = logging.getLogger(__name__)

def add_task(db: Session, *, current_user: models.User, description: str) -> models.Task:
    task = tasks_crud.create_task(db, user_id=current_user.id, description=description)
    logger.info("Task created successfully for user %s: %s", current_user.username, task.description)
    return task

def list_tasks(db: Session, *, current_user: models.User):
    return tasks_crud.list_for_user(db, user_id=current_user.id)

def update_task(db: Session, *, current_user: models.User, task_id: int, description=None, completed=None) -> models.Task:
    task = tasks_crud.update_task(db, user_id=current_user.id, task_id=task_id, description=description, completed=completed)
    logger.info("Task updated successfully for user %s: %s", current_user.username, task.description)
    return task

def delete_task(db: Session, *, current_user: models.User, task_id: int) -> None:
    tasks_crud.delete_task(db, user_id=current_user.id, task_id=task_id)
    logger.info("Task deleted successfully for user %s: Task ID %d", current_user.username, task_id)
    return None

def get_task(db: Session, *, current_user: models.User, task_id: int) -> models.Task:
    task = tasks_crud.get_owned(db, user_id=current_user.id, task_id=task_id)
    logger.info("Retrieved task for user %s: %s", current_user.username, task.description)
    return task

