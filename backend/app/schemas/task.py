from pydantic import BaseModel
from datetime import datetime
from app.models.task import TaskStatus

class TaskBase(BaseModel):
    title: str
    description: str | None = None

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: str | None = None
    description: str | None = None
    status: TaskStatus | None = None

class TaskAssign(BaseModel):
    assignee_id: int

class TaskInDB(TaskBase):
    id: int
    status: TaskStatus
    creator_id: int
    assignee_id: int | None = None
    created_at: datetime
    class Config:
        from_attributes = True
