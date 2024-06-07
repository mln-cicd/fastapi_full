from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.core.config import settings

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI), echo=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Ensure models are imported so they are registered with Base
# This is already done above with the imports of Post and User


def create_tables():
    Base.metadata.create_all(bind=engine)
