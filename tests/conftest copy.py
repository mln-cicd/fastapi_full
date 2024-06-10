import pytest
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.api.deps import get_db
from app.core.config import settings
from app.core.declarative import Base
from app.main import app

settings.ENVIRONMENT = "test"

logger.info(f"[DATABASE URI]: {settings.SQLALCHEMY_DATABASE_URI}")
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture()
def session():
    logger.info("Session fixture ran. Resetting...")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    
@pytest.fixture()
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    return TestClient(app)
    
@pytest.fixture()
def test_user(client):
    user_data = {"email": settings.TEST_EMAIL, "password": settings.TEST_PASSWORD}
    response = client.post(f"{settings.API_V1_STR}/users/", json=user_data)