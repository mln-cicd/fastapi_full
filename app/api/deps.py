from typing import Generator
from app.core.db import SessionLocal
from fastapi import Depends, HTTPException, status
from app.core.security import verify_access_token
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
import app.models.user as models


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# def get_db() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token = verify_access_token(
        token=token, credentials_exception=credentials_exception
    )
    user = db.query(models.User).filter(models.User.id == token.id).first()
    return user
