
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from tests.utils.docker import start_database_container, create_internal_network
from tests.const import PROJECT_DIR
from pathlib import Path
from tests.utils.database_utils import migrate_to_db
from python_on_whales import docker

settings.ENVIRONMENT = "test"

# PostgreSQL setup for integration tests
TEST_DATABASE_URL = "postgresql+psycopg2://postgres:postgres@localhost:35435/fastapi"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocalPostgres = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="session")
def docker_resources():
    # Create network
    create_internal_network()
    
    # Create volume
    volume = docker.volume.create("test-volume")
    
    # Start database container
    container = start_database_container()
    
    yield container
    
    # Teardown
    container.stop()
    container.remove()
    volume.remove()
    docker.network.remove("internal")

@pytest.fixture(scope="session")
def db_session(docker_resources):
    with engine.begin() as connection:
        migrate_to_db("migrations", Path(PROJECT_DIR / "alembic.ini").resolve(), connection)
        yield TestingSessionLocalPostgres()

@pytest.fixture()
def override_get_db(db_session):
    def override():
        return db_session

    app.dependency_overrides[get_db] = override
    yield
    app.dependency_overrides[get_db] = get_db

@pytest.fixture()
def client(override_get_db):
    with TestClient(app) as c:
        yield c