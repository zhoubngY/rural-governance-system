from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class AppStatus(str, Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ApplicationBase(BaseModel):
    type: str
    content: str

class ApplicationCreate(ApplicationBase):
    pass

class ApplicationUpdate(BaseModel):
    status: AppStatus
    admin_reply: Optional[str] = None

class ApplicationResponse(ApplicationBase):
    id: int
    user_id: int
    status: AppStatus
    admin_reply: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True