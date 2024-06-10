# tests/conftest.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from tests.utils.docker import start_database_container
from tests.const import PROJECT_DIR
from pathlib import Path
from tests.utils.database_utils import migrate_to_db

settings.ENVIRONMENT = "test"

# SQLite setup for unit tests
SQLALCHEMY_DATABASE_URL_SQLITE = "sqlite:///./test.db"
engine_sqlite = create_engine(SQLALCHEMY_DATABASE_URL_SQLITE, connect_args={"check_same_thread": False})
TestingSessionLocalSQLite = sessionmaker(autocommit=False, autoflush=False, bind=engine_sqlite)

# PostgreSQL setup for integration tests
engine_postgres = create_engine(settings.SQLALCHEMY_DATABASE_URI)
TestingSessionLocalPostgres = sessionmaker(autocommit=False, autoflush=False, bind=engine_postgres)

@pytest.fixture(scope="session")
def database_container():
    container = start_database_container()
    yield container
    container.stop()
    container.remove()

@pytest.fixture(scope="session")
def db_session_sqlite():
    with engine_sqlite.begin() as connection:
        yield TestingSessionLocalSQLite()

@pytest.fixture(scope="session")
def db_session_postgres(database_container):
    with engine_postgres.begin() as connection:
        migrate_to_db("migrations", Path(PROJECT_DIR / "alembic.ini").resolve(), connection)
        yield TestingSessionLocalPostgres()

@pytest.fixture()
def override_get_db_sqlite(db_session_sqlite):
    def override():
        return db_session_sqlite

    app.dependency_overrides[get_db] = override
    yield
    app.dependency_overrides[get_db] = get_db

@pytest.fixture()
def override_get_db_postgres(db_session_postgres):
    def override():
        return db_session_postgres

    app.dependency_overrides[get_db] = override
    yield
    app.dependency_overrides[get_db] = get_db

@pytest.fixture()
def client_sqlite(override_get_db_sqlite):
    with TestClient(app) as c:
        yield c

@pytest.fixture()
def client_postgres(override_get_db_postgres):
    with TestClient(app) as c:
        yield c