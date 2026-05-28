from typing import Annotated

from fastapi import APIRouter, Depends, Query, Response, status
from sqlalchemy.orm import Session

from app.db.session import get_session
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services.tasks import (
    create_task,
    delete_task,
    get_task,
    list_tasks,
    update_task,
)

router = APIRouter(prefix="/tasks", tags=["tasks"])
SessionDep = Annotated[Session, Depends(get_session)]
SkipQuery = Annotated[int, Query(ge=0)]
LimitQuery = Annotated[int, Query(ge=1, le=100)]


@router.post("", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def post_task(task: TaskCreate, session: SessionDep) -> TaskResponse:
    return create_task(session, task)


@router.get("", response_model=list[TaskResponse])
def get_tasks(
    session: SessionDep,
    skip: SkipQuery = 0,
    limit: LimitQuery = 100,
) -> list[TaskResponse]:
    return list_tasks(session, skip=skip, limit=limit)


@router.get("/{task_id}", response_model=TaskResponse)
def get_task_by_id(task_id: int, session: SessionDep) -> TaskResponse:
    return get_task(session, task_id)


@router.patch("/{task_id}", response_model=TaskResponse)
def patch_task(
    task_id: int,
    task: TaskUpdate,
    session: SessionDep,
) -> TaskResponse:
    return update_task(session, task_id, task)


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_task(task_id: int, session: SessionDep) -> Response:
    delete_task(session, task_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
