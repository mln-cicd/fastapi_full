from fastapi import FastAPI, Response, status, HTTPException, Depends
from loguru import logger
from typing import List
from sqlalchemy.orm import Session
import app.schemas as schemas
import app.models as models
from app.database import engine, get_db
from app.models import Base


Base.metadata.create_all(bind=engine)

app = FastAPI()

# ===========================================================
# ===========================================================

# ------------------CREATE----------------------------------


@app.post(
    "/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostRead
)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.post(
    "/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead
)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #   hashed_password = pwd_context.hash(user.password)
    #   user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# -----------------READ---------------------------------------


@app.get("/")
def get_healthcheck():
    return {"hotel": "trivago"}


@app.get("/posts/{post_id}", response_model=schemas.PostRead)
def get_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@app.get("/posts", response_model=List[schemas.PostRead])
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    db.delete(post)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# -----------------UPDATE--------------------------------------
@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostRead)
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
