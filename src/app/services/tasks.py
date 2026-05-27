from sqlalchemy.orm import Session

from app.repositories.tasks import TaskRepository
from app.schemas.task import TaskCreate, TaskResponse


def create_task(session: Session, task_create: TaskCreate) -> TaskResponse:
    repository = TaskRepository(session)
    task = repository.create(task_create)
    return TaskResponse.model_validate(task)


def list_tasks(session: Session) -> list[TaskResponse]:
    repository = TaskRepository(session)
    return [TaskResponse.model_validate(task) for task in repository.list()]
