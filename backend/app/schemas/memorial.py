from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class MemorialBase(BaseModel):
    title: str
    content: str
    happened_at: Optional[datetime] = None
    images: Optional[List[str]] = []

class MemorialCreate(MemorialBase):
    pass

class MemorialUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    happened_at: Optional[datetime] = None
    images: Optional[List[str]] = None

class MemorialResponse(MemorialBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True