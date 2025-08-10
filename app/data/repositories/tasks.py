from typing import Optional, List
from sqlalchemy.orm import Session
from .. import models
from sqlalchemy.exc import SQLAlchemyError
from ...core.errors import TaskNotFoundError, TaskForbiddenError, DatabaseError
# CRUD operations for Task model

def create_task(db: Session, *, user_id: int, description: str) -> models.Task:
    """
    Create a new task for the given user.
    Commits the transaction and returns the persisted Task.
    Raises:
      - DatabaseError on DB failures (handled globally).
    """
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
    """
    Return all tasks owned by user_id.
    """
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_owned(db: Session, *, user_id: int, task_id: int) -> models.Task:
    """
    Load a task by id and ensure it belongs to user_id.
    Raises:
      - TaskNotFoundError if it doesn't exist
      - TaskForbiddenError if owned by a different user
    """
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise TaskNotFoundError(task_id)
    if task.user_id != user_id:
        raise TaskForbiddenError()
    return task

def update_task(db: Session, *, user_id: int, task_id: int, description=None, completed=None) -> models.Task:
    """
    Partially update a task (description/completed) if owned by user_id.
    Commits and returns the updated Task.
    Raises:
      - TaskNotFoundError / TaskForbiddenError via get_owned()
      - DatabaseError on DB failures
    """
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
    """
    Delete a task if owned by user_id.
    Raises:
      - TaskNotFoundError / TaskForbiddenError via get_owned()
      - DatabaseError on DB failures
    """
    task = get_owned(db, user_id=user_id, task_id=task_id)
    try:
        db.delete(task)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError() from e
