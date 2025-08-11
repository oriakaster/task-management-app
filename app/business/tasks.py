import logging
from sqlalchemy.orm import Session
from ..data import models
from ..data.repositories import tasks as tasks_crud

logger = logging.getLogger(__name__)

def add_task(db: Session, *, current_user: models.User, description: str) -> models.Task:
    """input: description of the task to be added
        output: the created task object 
        Create and persist a new task for the given user"""
    task = tasks_crud.create_task(db, user_id=current_user.id, description=description)
    logger.info("Task created successfully for user %s: %s", current_user.username, task.description)
    return task

def list_tasks(db: Session, *, current_user: models.User):
    """input: current user
       output: list of tasks for the user
       List all tasks for the given user"""
    list_tasks = tasks_crud.list_for_user(db, user_id=current_user.id) 
    logger.info("Listed tasks for user %s: %d tasks found", current_user.username, len(list_tasks))  
    return list_tasks

def update_task(db: Session, *, current_user: models.User, task_id: int, description=None, completed=None) -> models.Task:
    """input: current user, task_id, optional description and completed status
       output: the updated task object
       Update an existing task for the given user"""
    task = tasks_crud.update_task(db, user_id=current_user.id, task_id=task_id, description=description, completed=completed)
    logger.info("Task updated successfully for user %s: %s", current_user.username, task.description)
    return task

def delete_task(db: Session, *, current_user: models.User, task_id: int) -> None:
    """input: current user, task_id
       output: None
       Delete a task for the given user"""
    tasks_crud.delete_task(db, user_id=current_user.id, task_id=task_id)
    logger.info("Task deleted successfully for user %s: Task ID %d", current_user.username, task_id)
    return None

def get_task(db: Session, *, current_user: models.User, task_id: int) -> models.Task:
    """input: current user, task_id
       output: the task object
       Retrieve a specific task for the given user"""
    task = tasks_crud.get_owned(db, user_id=current_user.id, task_id=task_id)
    logger.info("Retrieved task for user %s: %s", current_user.username, task.description)
    return task

