from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PolicyBase(BaseModel):
    title: str
    content: str
    category: Optional[str] = None

class PolicyCreate(PolicyBase):
    published_at: Optional[datetime] = None

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    category: Optional[str] = None
    published_at: Optional[datetime] = None

class PolicyInDB(PolicyBase):
    id: int
    published_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
