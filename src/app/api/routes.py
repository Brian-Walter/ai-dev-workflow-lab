from fastapi import APIRouter

from app.api.tasks import router as tasks_router
from app.schemas.health import HealthResponse
from app.schemas.root import RootResponse
from app.services.status import get_health_status, get_root_message

router = APIRouter()
router.include_router(tasks_router)


@router.get("/", response_model=RootResponse)
def root() -> RootResponse:
    return RootResponse(message=get_root_message())


@router.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status=get_health_status())
