from datetime import datetime

from pydantic import BaseModel, EmailStr


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
        from_attrubutes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str
