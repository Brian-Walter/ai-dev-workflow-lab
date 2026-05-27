from fastapi import FastAPI

from app.api.routes import router
from app.core.config import settings
from app.core.exceptions import register_exception_handlers
from app.core.logging import configure_logging
from app.core.middleware import RequestLoggingMiddleware
from app.db.migrations import run_migrations


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title=settings.app_title)
    app.add_middleware(RequestLoggingMiddleware)
    register_exception_handlers(app)
    app.include_router(router)
    run_migrations()
    return app


app = create_app()
