from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.declarative import Base

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def create_tables():
    """Create all tables from metadata (DEACTIVATE WHEN USING ALEMBIC MIGRATIONS)"""
    Base.metadata.create_all(bind=engine)
