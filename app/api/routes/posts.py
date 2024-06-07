from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
import app.schemas.posts as schemas
import app.models.post as models
from app.api.deps import get_db
from loguru import logger

router = APIRouter()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRead)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


# -----------------READ---------------------------------------
@router.get("/", response_model=List[schemas.PostRead])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@router.get("/{id}", response_model=schemas.PostRead)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Post not found"
        )
    return post


# -----------------UPDATE--------------------------------------


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostRead)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    logger.info(f"Received data: {post}")
    post_query = db.query(models.Post).filter(models.Post.id == id)
    existing_post = post_query.first()
    if existing_post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    post_query.update(post.model_dump(), synchronize_session=False)
    db.commit()
    return post_query.first()


# -------------------DELETE-------------------------------------


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
