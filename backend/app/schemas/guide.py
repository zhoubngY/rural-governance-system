from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class GuideBase(BaseModel):
    title: str
    content: str
    order: int = 0

class GuideCreate(GuideBase):
    pass

class GuideUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    order: Optional[int] = None

class GuideResponse(GuideBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True