from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    app_title: str = "AI Dev Workflow Lab API"
    database_url: str = "sqlite:///./app.db"


settings = Settings()
