from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session

from typing import List
import app.schemas.users as schemas
import app.models.user as models
from app.api.deps import get_db, get_current_user
from app.core.security import pwd_context
from loguru import logger


router = APIRouter()


# ------------------CREATE----------------------------------


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserRead)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# -----------------READ---------------------------------------


@router.get("/", response_model=List[schemas.UserRead])
def get_users(db: Session = Depends(get_db)):
    users = db.query(models.User).all()
    return users


@router.get("/{id}", response_model=schemas.UserRead)
def get_user(
    id: int,
    current_user: int = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


# -----------------UPDATE--------------------------------------


@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.UserRead)
def update_user(
    id: int,
    user: schemas.UserCreate,
    current_user=Depends(get_current_user),
    db: Session = Depends(get_db),
):
    logger.info(f"Received data: {user}")
    user_query = db.query(models.User).filter(models.User.id == id)
    existing_user = user_query.first()
    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found"
        )
    user_query.update(user.model_dump(), synchronize_session=False)
    db.commit()
    return user_query.first()


# -------------------DELETE-------------------------------------


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: int, current_user=Depends(get_current_user), db: Session = Depends(get_db)
):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found"
        )
    db.delete(user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
