import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer
from app.api.deps import get_db
from app.main import app
from app.core.db import create_tables  # Import the create_tables function

# Set up the Postgres container
POSTGRES_IMAGE = "postgres:16.1-alpine3.19"
POSTGRES_USERNAME = "postgres"
POSTGRES_PASSWORD = "postgres"
POSTGRES_DATABASE = "localhost:5434/testdb"

@pytest.fixture(scope="session")
def postgres_container():
    """
    Setup Postgres container.
    """
    with PostgresContainer(
        POSTGRES_IMAGE,
        username=POSTGRES_USERNAME,
        password=POSTGRES_PASSWORD,
        dbname="localhost:5434/testdb",
    ) as postgres:
        postgres.start()
        yield postgres

@pytest.fixture(scope="function")
def db_session(postgres_container):
    """
    Create a new database session for each test.
    """
    engine = create_engine(postgres_container.get_connection_url())
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    # Ensure the database connection is established
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))
    except Exception as e:
        raise RuntimeError("Failed to connect to the database") from e

    # Create tables
    create_tables()

    yield SessionLocal

    engine.dispose()

@pytest.fixture(scope="function")
def client(db_session):
    """
    Create a test client fixture that overrides the dependency to use the test database.
    """
    def override_get_db():
        db = db_session()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as _client:
        yield _client
    app.dependency_overrides[get_db] = get_db