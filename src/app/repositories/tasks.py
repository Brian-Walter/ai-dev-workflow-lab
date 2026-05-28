from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


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

    def get(self, task_id: int) -> Task | None:
        return self._session.get(Task, task_id)

    def list(self, skip: int = 0, limit: int = 100) -> list[Task]:
        statement = select(Task).order_by(Task.id).offset(skip).limit(limit)
        tasks = self._session.scalars(statement).all()
        return list(tasks)

    def update(self, task: Task, task_update: TaskUpdate) -> Task:
        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        self._session.commit()
        self._session.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self._session.delete(task)
        self._session.commit()
