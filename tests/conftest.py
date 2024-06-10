import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.main import start_application
from app.core.db import Base, create_tables


app = start_application(environment="sqlite_test")
# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="function")
def db_engine():
    """
    Create a new database engine for each test.
    """
    engine = create_engine(SQLALCHEMY_DATABASE_URL)
    yield engine
    engine.dispose()

@pytest.fixture(scope="function")
def db_session(db_engine):
    """
    Create a new database session for each test.
    """
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = SessionLocal()

    # Create tables before yielding the session
    create_tables()

    yield session
    session.close()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client fixture that overrides the dependency to use the test database.
    """
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides[get_db] = get_db