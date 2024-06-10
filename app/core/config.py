# app/core/config.py

import secrets
from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import EmailStr
from pydantic_settings import BaseSettings  # , AnyUrl


class Settings(BaseSettings):
    """Application settings."""

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    class Config:
        case_sensitive = True  # Set to True to match the exact case of environment variables

    BACKEND_CORS_ORIGINS: Union[str, List[str]] = "*"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "test", "staging", "production"] = "local"
    PROJECT_NAME: str = "FastAPI FULL"

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        if self.ENVIRONMENT == "local":
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}/{self.POSTGRES_DB}"
        elif self.ENVIRONMENT == "test":
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}_test"
        elif self.ENVIRONMENT == "unit_test":
            return "sqlite:///./test.db"
        elif self.ENVIRONMENT == "integration_test":
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@localhost/{self.POSTGRES_DB}_integration_test"
        elif self.ENVIRONMENT == "production":
            return f"postgresql+psycopg2://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@production-db-host/{self.POSTGRES_DB}"
        else:
            raise ValueError(f"Unknown environment: {self.ENVIRONMENT}")

    TEST_EMAIL: Optional[EmailStr] = "test_user@example.com"
    TEST_PASSWORD: Optional[str] = "testpassword123"
    FIRST_SUPERUSER: Optional[str] = ""
    FIRST_SUPERUSER_PASSWORD: Optional[str] = ""
    # # More configurations can be added here in the future

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