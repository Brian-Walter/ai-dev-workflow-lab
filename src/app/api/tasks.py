from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskResponse
from app.services.tasks import create_task, list_tasks

router = APIRouter(prefix="/tasks", tags=["tasks"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_task(task: TaskCreate, session: SessionDep) -> TaskResponse:
    return create_task(session, task)


@router.get("", response_model=list[TaskResponse])
def get_tasks(session: SessionDep) -> list[TaskResponse]:
    return list_tasks(session)
