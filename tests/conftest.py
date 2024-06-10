import pytest
from fastapi.testclient import TestClient
from loguru import logger
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.api.deps import get_db
from app.core.config import settings
from app.main import app
from tests.utils.docker import start_database_container
from tests.const import PROJECT_DIR
from pathlib import Path
from tests.utils.database_utils import migrate_to_db
from app.main import start_application

settings.ENVIRONMENT = "test"

logger.info(f"[DATABASE URI]: {settings.SQLALCHEMY_DATABASE_URI}")


logger.info(f"[DATABASE URI]: {settings.SQLALCHEMY_DATABASE_URI}")
engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="session")
def database_container():
    container = start_database_container()
    yield container
    container.stop()
    container.remove()




@pytest.fixture(scope="session")
def db_session():
    container = database_container()
    engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
    
    with engine.begin() as connection:
        migrate_to_db("migrations", Path(PROJECT_DIR / "alembic.ini").resolve(), connection)
        
        SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)
        yield SessionLocal
        
        engine.dispose()
        

@pytest.fixture()
def override_get_db_session(db_session):
    def override():
        return db_session
    
    app.dependency_overrides[get_db] = override
       
@pytest.fixture()
def client(override_get_db_session):
    with TestClient(app) as _client:
        yield _client