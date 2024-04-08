import os

from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.ext.asyncio import AsyncEngine


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file="settings/envs/.env-common", env_file_encoding="utf-8")

    app_name: str = "Provider Events Sync"
    app_version: str = "0.0.1"

    ENV: str = "dev"
    LOG_LEVEL: str = "INFO"

    DB_URL: str = "sqlite+aiosqlite:///./provider_events.sqlite"  # SQLite in memory by default
    TEST_DB_URL: str = "sqlite+aiosqlite://"  # SQLite in memory by default
    DB_ENGINE: AsyncEngine | None = None

    EVENTS_SYNC_DELAY_SECONDS: int = 60


CACHED_SETTINGS: Settings | None = None


def get_settings(env: str | None = None, reload=False) -> Settings:
    global CACHED_SETTINGS  # pylint: disable=global-statement
    if not CACHED_SETTINGS or reload:
        if env is None:
            env = os.getenv("PROVIDER_EVENTS_ENV", "dev")
        env_files = []
        if env != "dev" and os.path.exists(f"settings/envs/.env-{env}"):
            env_files.append(f"settings/envs/.env-{env}")
        if os.path.exists(".env-local"):
            env_files.append(".env-local")
        CACHED_SETTINGS = Settings(_env_file=tuple(env_files))  # type: ignore

    return CACHED_SETTINGS


def get_env():
    return get_settings().ENV
