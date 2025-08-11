from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models
from sqlalchemy.exc import SQLAlchemyError
from ...core.errors import TaskNotFoundError, TaskForbiddenError, DatabaseError

def create_task(db: Session, *, user_id: int, description: str) -> models.Task:
    """input: user_id, description
        output: Task object
        Creates a new task for the given user_id with the provided description."""
    task = models.Task(user_id=user_id, description=description, completed=False)
    try:
        db.add(task)
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError() from e

def list_for_user(db: Session, *, user_id: int) -> List[models.Task]:
    """input: user_id
       output: List of Task objects
       Lists all tasks owned by the given user_id."""
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_owned(db: Session, *, user_id: int, task_id: int) -> models.Task:
    """input: user_id, task_id
       output: Task object
       Retrieves a task owned by user_id with the given task_id.
       Raises:
         - TaskNotFoundError if task does not exist
         - TaskForbiddenError if task exists but is not owned by user_id"""
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    if task.user_id != user_id:
        raise TaskForbiddenError()
    return task

def update_task(db: Session, *, user_id: int, task_id: int, description=None, completed=None) -> models.Task:
    """input: user_id, task_id, description=None, completed=None
       output: Task object
       Updates a task owned by user_id with the given task_id."""
    task = get_owned(db, user_id=user_id, task_id=task_id)

    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = bool(completed)
    try:
        db.commit()
        db.refresh(task)
        return task
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError() from e

def delete_task(db: Session, *, user_id: int, task_id: int) -> None:
    """input: user_id, task_id
       output: None
       Deletes a task owned by user_id with the given task_id."""
    task = get_owned(db, user_id=user_id, task_id=task_id)
    try:
        db.delete(task)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError() from e
