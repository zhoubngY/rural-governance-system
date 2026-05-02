from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class NoticeBase(BaseModel):
    title: str
    content: str
    is_top: bool = False
    published_at: Optional[datetime] = None

class NoticeCreate(NoticeBase):
    pass

class NoticeUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    is_top: Optional[bool] = None
    published_at: Optional[datetime] = None

class NoticeResponse(NoticeBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True