from typing import Any, Dict, Literal, Optional
from pydantic_settings import BaseSettings  # , AnyUrl

import secrets


class Settings(BaseSettings):
    """
    Application settings.
    """

    postgres_user: Optional[str] = None
    postgres_password: Optional[str] = None
    postgres_host: Optional[str] = None
    postgres_db: Optional[str] = None
    superset_admin_username: Optional[str] = None
    superset_admin_password: Optional[str] = None
    superset_secret_key: Optional[str] = None

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = "FastAPI FULL"
    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+psycopg2://postgres:postgres@127.0.0.1:35433/fastapi"
    )

    # More configurations can be added here in the future

    def as_dict(self) -> Dict[str, Any]:
        return self.dict()

    @classmethod
    def from_dict(cls, settings_dict: Dict[str, Any]) -> "Settings":
        return cls(**settings_dict)

    @classmethod
    def load(cls) -> "Settings":
        return cls()

    @classmethod
    def load_from_dict(cls, settings_dict: Dict[str, Any]) -> "Settings":
        return cls.from_dict(settings_dict)


settings = Settings.load()
