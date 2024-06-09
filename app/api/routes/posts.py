from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from loguru import logger
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db
from app.models.post import Post
from app.models.user import User
from app.models.vote import Vote
from app.schemas.posts import PostCreate, PostRead, PostWithVote

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostRead)
def create_post(
    post: PostCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    new_post = Post(owner_id=current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# -----------------READ---------------------------------------
@router.get("/", response_model=List[PostWithVote])
def get_posts(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
    limit: int = 10,
    skip: int = 2,
    search: str | None = "",
):
    logger.info(f"\n\nFROM get_posts\ncurrent_user.id: {current_user.id}")
    posts = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        # .filter(Post.owner_id == current_user.id) # Comment this line to get fr private to pblic
        .filter(Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )

    logger.info(f"\n\nFROM get_posts\posts: {posts}")
    return posts


@router.get("/{id}", response_model=PostWithVote)
def get_post(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = (
        db.query(Post, func.count(Vote.post_id).label("votes"))
        .join(Vote, Vote.post_id == Post.id, isouter=True)
        .group_by(Post.id)
        .filter(Post.id == id)
        .first()
    )  # add to get private posts .filter(Post.owner_id == current_user.id)\
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")
    return post


# -----------------UPDATE--------------------------------------


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=PostRead)
def update_post(
    id: int,
    post: PostCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(f"Received data: {post}")
    post_query = db.query(Post).filter(Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if existing_post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post",
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# -------------------DELETE-------------------------------------


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    post = db.query(Post).filter(Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post",
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
