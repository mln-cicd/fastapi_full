from pydantic import BaseModel
from datetime import datetime


class PostBase(BaseModel):
    title: str
    content: str
    published: bool | None = True


class PostCreate(PostBase):
    rating: int | None = None


class PostUpdate(PostBase):
    rating: int | None = None


class PostRead(BaseModel):
    id: int
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        orm_mode = True
