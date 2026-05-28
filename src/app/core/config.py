import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_title: str
    environment: str
    database_url: str
    log_level: str


def load_settings() -> Settings:
    return Settings(
        app_title=os.getenv("APP_TITLE", "AI Dev Workflow Lab API"),
        environment=os.getenv("APP_ENV", "development"),
        database_url=os.getenv("DATABASE_URL", "sqlite:///./app.db"),
        log_level=os.getenv("LOG_LEVEL", "INFO").upper(),
    )


settings = load_settings()
