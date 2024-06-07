from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserBase(BaseModel):
    name: str
    email: EmailStr
    password: str


class UserCreate(UserBase):
    pass


class UserRead(BaseModel):
    name: str
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True
