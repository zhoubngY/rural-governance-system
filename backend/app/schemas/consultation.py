from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from enum import Enum

class ConsultStatus(str, Enum):
    pending = "pending"
    answered = "answered"

class ConsultationBase(BaseModel):
    question: str

class ConsultationCreate(ConsultationBase):
    pass

class ConsultationUpdate(BaseModel):
    answer: str

class ConsultationResponse(ConsultationBase):
    id: int
    user_id: int
    answer: Optional[str]
    status: ConsultStatus
    created_at: datetime

    class Config:
        from_attributes = True