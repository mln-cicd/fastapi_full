from typing import Generator
from app.core.db import SessionLocal


def get_db() -> Generator:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


# def get_db() -> Generator[Session, None, None]:
#     with Session(engine) as session:
#         yield session
