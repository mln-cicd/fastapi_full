from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
import app.models.user as models
from app.api.deps import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token

router = APIRouter()


@router.post("/")
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    """_summary_

    Args:
        user_credentials (schemas.UserLogin): _description_
        db (Session, optional): _description_. Defaults to Depends(get_db).
    """
    user = (
        db.query(models.User)
        .filter(models.User.name == user_credentials.username)
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    verified = verify_password(user_credentials.password, user.password)
    if not verified:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User not found"
        )

    access_token = create_access_token(data={"username": user.name})
    return {"access_token": access_token, "token_type": "bearer"}
