from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    username: str
    full_name: str | None = None
    village_id: int

class UserCreatePublic(UserBase):
    password: str

class UserCreate(UserBase):
    password: str
    role: str = "villager"

class UserUpdate(BaseModel):
    full_name: str | None = None
    role: str | None = None

class UserInDB(UserBase):
    id: int
    role: str
    created_at: datetime
    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    role: Optional[str] = None