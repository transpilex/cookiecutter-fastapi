import os
from pathlib import Path
from dotenv import load_dotenv
from typing import List
from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load environment variables from the .env file in the root directory
ENV_PATH = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(dotenv_path=ENV_PATH)

class AppSettings(BaseSettings):
    STATIC_URL: str = "/static"
    STATIC_DIR: str = "apps/static"
    TEMPLATES_DIR: str = "apps/templates"


class SecuritySettings(BaseSettings):
    # Environment: "development" | "production"
    ENVIRONMENT: str = "development"

    # Trusted hosts — comma-separated, e.g. "example.com,www.example.com"
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # CORS origins — comma-separated, e.g. "https://example.com"
    CORS_ORIGINS: List[str] = ["http://localhost", "http://127.0.0.1"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # Set True in production to redirect HTTP → HTTPS
    HTTPS_REDIRECT: bool = False


class DatabaseSettings(BaseSettings):
    pass


class SQLiteSettings(DatabaseSettings):
    SQLITE_URI: str = "./sql_app.db"
    SQLITE_SYNC_PREFIX: str = "sqlite:///"
    SQLITE_ASYNC_PREFIX: str = "sqlite+aiosqlite:///"


class MySQLSettings(DatabaseSettings):
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_SERVER: str = "localhost"
    MYSQL_PORT: int = 5432
    MYSQL_DB: str
    MYSQL_SYNC_PREFIX: str = "mysql://"
    MYSQL_ASYNC_PREFIX: str = "mysql+aiomysql://"
    MYSQL_URL: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def MYSQL_URI(self) -> str:
        credentials = f"{self.MYSQL_USER}:{self.MYSQL_PASSWORD}"
        location = f"{self.MYSQL_SERVER}:{self.MYSQL_PORT}/{self.MYSQL_DB}"
        return f"{credentials}@{location}"


class PostgresSettings(DatabaseSettings):
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_SERVER: str = "localhost"
    POSTGRES_PORT: int = 3306
    POSTGRES_DB: str
    POSTGRES_SYNC_PREFIX: str = "postgresql://"
    POSTGRES_ASYNC_PREFIX: str = "postgresql+asyncpg://"
    POSTGRES_URL: str | None = None

    @computed_field  # type: ignore[prop-decorator]
    @property
    def POSTGRES_URI(self) -> str:
        credentials = f"{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
        location = f"{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return f"{credentials}@{location}"


class Settings(
    AppSettings,
    SecuritySettings,
    SQLiteSettings,
    MySQLSettings,
    PostgresSettings
):
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",
    )


settings = Settings()
