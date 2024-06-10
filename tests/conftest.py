
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.main import app
from tests.utils.docker import start_database_container
from tests.const import PROJECT_DIR


# PostgreSQL setup for integration tests
TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:35435/fastapi"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocalPostgres = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def db_session():
    container = start_database_container()

    engine = create_engine(TEST_DATABASE_URL)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    yield SessionLocal

    container.stop()
    container.remove()
    engine.dispose()

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        return db_session()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides[get_db] = get_db