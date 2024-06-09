from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

import app.models.user as models
import app.schemas.tokens as schemas
from app.api.deps import get_db
from app.core.security import create_access_token, verify_password

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(models.User.name == user_credentials.username).first()
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials")

    access_token = create_access_token(data={"user_id": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
