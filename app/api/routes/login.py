from fastapi import APIRouter, Depends, Response, status, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.schemas import users as schemas
import app.models.user as models
from app.api.deps import get_db
from app.core.security import verify_password
from loguru import logger

router = APIRouter()

@router.post("/")
def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
    """_summary_

    Args:
        user_credentials (schemas.UserLogin): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """    
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    verified = verify_password(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User not found")
    
    