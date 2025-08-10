from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import schemas
from ..authentication import get_current_user
from ..data import models
from ..business import tasks as tasks_service

# Purpose: Router for task-related endpoints
router = APIRouter(prefix="/tasks")

@router.post("", response_model=schemas.TaskOut)
def add_task(task_in: schemas.TaskCreate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.add_task(db, current_user=current_user, description=task_in.description)

@router.get("", response_model=List[schemas.TaskOut])
def list_tasks(db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.list_tasks(db, current_user=current_user)

@router.put("/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_up: schemas.TaskUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    return tasks_service.update_task(
        db,
        current_user=current_user,
        task_id=task_id,
        description=task_up.description,
        completed=task_up.completed,
    )

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    tasks_service.delete_task(db, current_user=current_user, task_id=task_id)
    return {"message": "Task deleted successfully"}
