from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    real_name: Optional[str] = None
    phone: Optional[str] = None
    role: str
    village_id: int
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class UserCreatePublic(UserBase):
    password: str
    role: Optional[str] = "villager"
    
class UserUpdate(BaseModel):
    real_name: Optional[str] = None
    phone: Optional[str] = None
    role: Optional[str] = None
    is_active: Optional[bool] = None

class UserInDB(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True