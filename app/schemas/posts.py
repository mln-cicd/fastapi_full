from datetime import datetime

from pydantic import BaseModel

from app.schemas.users import UserRead


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
    owner_id: int
    owner: UserRead
    title: str
    content: str
    published: bool = True
    created_at: datetime

    class Config:
        from_attrubutes = True


class PostWithVote(BaseModel):
    Post: PostRead  # or maybe Post: PostRead
    votes: int

    class Config:
        from_attributes = True
