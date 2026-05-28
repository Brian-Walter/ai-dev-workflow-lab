from sqlalchemy import inspect, text

from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers tables before create_all runs.
from app.models import task  # noqa: F401


def run_migrations() -> None:
    Base.metadata.create_all(bind=engine)
    _ensure_task_timestamps()


def _ensure_task_timestamps() -> None:
    if engine.dialect.name != "sqlite":
        return

    inspector = inspect(engine)
    if not inspector.has_table("tasks"):
        return

    columns = {column["name"] for column in inspector.get_columns("tasks")}
    missing_columns = {"created_at", "updated_at"} - columns
    if not missing_columns:
        return

    with engine.begin() as connection:
        for column_name in sorted(missing_columns):
            connection.execute(
                text(f"ALTER TABLE tasks ADD COLUMN {column_name} DATETIME")
            )
            connection.execute(
                text(
                    "UPDATE tasks "
                    f"SET {column_name} = CURRENT_TIMESTAMP "
                    f"WHERE {column_name} IS NULL"
                )
            )
