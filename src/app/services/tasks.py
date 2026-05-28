from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundError
from app.repositories.tasks import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate


def create_task(session: Session, task_create: TaskCreate) -> TaskResponse:
    repository = TaskRepository(session)
    task = repository.create(task_create)
    return TaskResponse.model_validate(task)


def get_task(session: Session, task_id: int) -> TaskResponse:
    repository = TaskRepository(session)
    task = repository.get(task_id)
    if task is None:
        raise NotFoundError("Task not found")
    return TaskResponse.model_validate(task)


def list_tasks(session: Session, skip: int = 0, limit: int = 100) -> list[TaskResponse]:
    repository = TaskRepository(session)
    return [
        TaskResponse.model_validate(task)
        for task in repository.list(skip=skip, limit=limit)
    ]


def update_task(
    session: Session,
    task_id: int,
    task_update: TaskUpdate,
) -> TaskResponse:
    repository = TaskRepository(session)
    task = repository.get(task_id)
    if task is None:
        raise NotFoundError("Task not found")

    updated_task = repository.update(task, task_update)
    return TaskResponse.model_validate(updated_task)


def delete_task(session: Session, task_id: int) -> None:
    repository = TaskRepository(session)
    task = repository.get(task_id)
    if task is None:
        raise NotFoundError("Task not found")

    repository.delete(task)
