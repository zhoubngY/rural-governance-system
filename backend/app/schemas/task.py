from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    priority: str = "medium"
    due_date: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = Field(default_factory=dict)

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    due_date: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

class TaskAssign(BaseModel):
    assignee_id: int

class TaskInDB(TaskBase):
    id: int
    status: str
    creator_id: int
    created_at: datetime
    assignee_id: Optional[int] = None
    assignee_name: Optional[str] = None
    creator_name: Optional[str] = None

    class Config:
        from_attributes = True