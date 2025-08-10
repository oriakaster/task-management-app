from sqlalchemy.orm import Session
from ..data import models
from ..data.repositories import tasks as tasks_crud

# Service Layer for task management, including adding, listing, updating, and deleting tasks

def add_task(db: Session, *, current_user: models.User, description: str) -> models.Task:
    return tasks_crud.create_task(db, user_id=current_user.id, description=description)

def list_tasks(db: Session, *, current_user: models.User):
    return tasks_crud.list_for_user(db, user_id=current_user.id)

def update_task(db: Session, *, current_user: models.User, task_id: int, description=None, completed=None) -> models.Task:
    return tasks_crud.update_task(db, user_id=current_user.id, task_id=task_id, description=description, completed=completed)

def delete_task(db: Session, *, current_user: models.User, task_id: int) -> None:
    return tasks_crud.delete_task(db, user_id=current_user.id, task_id=task_id)

def get_task(db: Session, *, current_user: models.User, task_id: int) -> models.Task | None:
    return tasks_crud.get(db, user_id=current_user.id, task_id=task_id)

