from pydantic import BaseModel, validator
from datetime import datetime
from typing import Optional, Dict, Any, List
import json

class NoteCreate(BaseModel):
    type: str
    title: str
    content: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    @validator('type', pre=True, always=True)
    def lower_type(cls, v):
        return v.lower() if v else v

class NoteUpdate(BaseModel):
    type: Optional[str] = None
    title: Optional[str] = None
    content: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None

    @validator('type', pre=True, always=True)
    def lower_type(cls, v):
        return v.lower() if v else v

class NoteInDB(BaseModel):
    id: int
    type: str
    title: str
    content: Optional[str] = None
    extra_data: Optional[Dict[str, Any]] = None
    user_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    @validator('extra_data', pre=True, always=True)
    def parse_extra_data(cls, v):
        if isinstance(v, str):
            try:
                return json.loads(v)
            except:
                return None
        return v

    class Config:
        from_attributes = True

# 分页响应模型
class NoteListResponse(BaseModel):
    items: List[NoteInDB]
    total: int
    page: int
    page_size: int
    pages: int