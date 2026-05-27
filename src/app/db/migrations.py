from app.db.base import Base
from app.db.session import engine

# Import models so SQLAlchemy registers tables before create_all runs.
from app.models import task  # noqa: F401


def run_migrations() -> None:
    Base.metadata.create_all(bind=engine)
