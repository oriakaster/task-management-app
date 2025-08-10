from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from .. import models
# CRUD operations for Task model

def create_task(db: Session, *, user_id: int, description: str) -> models.Task:
    task = models.Task(user_id=user_id, description=description, completed=False)
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

def list_for_user(db: Session, *, user_id: int):
    return db.query(models.Task).filter(models.Task.user_id == user_id).all()

def get_owned(db: Session, *, user_id: int, task_id: int) -> models.Task:
    task = db.query(models.Task).filter(models.Task.id == task_id).first()
    if not task:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    if task.user_id != user_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not allowed")
    return task

def update_task(db: Session, *, user_id: int, task_id: int, description=None, completed=None) -> models.Task:
    task = get_owned(db, user_id=user_id, task_id=task_id)
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = bool(completed)
    db.commit()
    db.refresh(task)
    return task

def delete_task(db: Session, *, user_id: int, task_id: int) -> None:
    task = get_owned(db, user_id=user_id, task_id=task_id)
    db.delete(task)
    db.commit()
