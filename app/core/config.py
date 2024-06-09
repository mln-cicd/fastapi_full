import secrets
from typing import Any, Dict, Literal, Optional

from pydantic_settings import BaseSettings  # , AnyUrl


class Settings(BaseSettings):
    """Application settings."""

    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    class Config:
        case_sensitive = True  # Set to True to match the exact case of environment variables

    BACKEND_CORS_ORIGINS: bool | None = True
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60  # * 24 * 8
    DOMAIN: str = "localhost"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    PROJECT_NAME: str = "FastAPI FULL"
    SQLALCHEMY_DATABASE_URI: str = (
        "postgresql+psycopg2://postgres:postgres@127.0.0.1:35433/fastapi"
    )

    # @property
    # def SQLALCHEMY_DATABASE_URI(self) -> str:
    #     if self.ENVIRONMENT == "local":
    #         return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}/{self.postgres_db}"
    #     elif self.ENVIRONMENT == "staging":
    #         return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@staging-db-host/{self.postgres_db}"
    #     elif self.ENVIRONMENT == "production":
    #         return f"postgresql+psycopg2://{self.postgres_user}:{self.postgres_password}@production-db-host/{self.postgres_db}"
    #     else:
    #         raise ValueError(f"Unknown environment: {self.ENVIRONMENT}")

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
