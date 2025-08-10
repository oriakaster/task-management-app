from pydantic import BaseModel
from typing import Optional

# -------- Tasks --------
class TaskBase(BaseModel):
    description: Optional[str] = None
    completed: Optional[bool] = None

class TaskCreate(BaseModel):
    description: str

class TaskUpdate(TaskBase):
    pass  # partial updates allowed

class TaskOut(BaseModel):
    id: int
    user_id: int
    description: str
    completed: bool
    
    class Config:
        from_attributes = True
