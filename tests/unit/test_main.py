from fastapi.testclient import TestClient
from loguru import logger

from app.api.main import api_router
from app.core.config import settings
from app.core.db import SessionLocal
from app.core.declarative import Base
from app.schemas.users import UserRead

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables from metadata (DEACTIVATE WHEN USING ALEMBIC MIGRATIONS)"""
    Base.metadata.create_all(bind=engine)


def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


client = TestClient(api_router)


def test_root():
    res = client.get("/")
    logger.info("Message:", res.json().get("message"))  # Print the message for debugging purposes
    assert res.json().get("message") == "ok"
    assert res.status_code == 200


def test_create_user():
    res = client.post(
        "/users/",
        json={"email": "hello123@gmail.com", "name": "pierrick", "password": "password123"},
    )
    new_user = UserRead(**res.json())
    logger.info(res.json())
    assert res.status_code == 201
    assert res.json().get("email") == "hello123@gmail.com"
