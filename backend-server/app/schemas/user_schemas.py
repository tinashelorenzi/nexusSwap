from pydantic import BaseModel, EmailStr
from typing import Optional
from ..models.models import UserRole

class UserBase(BaseModel):
    email: EmailStr
    username: str

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    email: Optional[EmailStr] = None
    username: Optional[str] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None
    is_blocked: Optional[bool] = None

class User(UserBase):
    id: int
    role: UserRole
    is_active: bool
    is_blocked: bool

    class Config:
        from_attributes = True 