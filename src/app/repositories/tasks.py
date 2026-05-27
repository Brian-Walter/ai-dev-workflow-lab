from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate


class TaskRepository:
    def __init__(self, session: Session) -> None:
        self._session = session

    def create(self, task_create: TaskCreate) -> Task:
        task = Task(
            title=task_create.title,
            description=task_create.description,
            completed=False,
        )
        self._session.add(task)
        self._session.commit()
        self._session.refresh(task)
        return task

    def list(self) -> list[Task]:
        tasks = self._session.scalars(select(Task).order_by(Task.id)).all()
        return list(tasks)
