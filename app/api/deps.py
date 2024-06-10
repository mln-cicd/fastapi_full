from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

import app.models.user as models
from app.core.db import SessionLocal
from app.core.security import verify_access_token, oauth2_scheme


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# def get_db() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session




def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token=token, credentials_exception=credentials_exception)
    user = db.query(models.User).filter(models.User.id == int(token_data.id)).first()
    if user is None:
        raise credentials_exception
    return user
