from collections.abc import Generator
from datetime import datetime

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_session
from app.main import app
from app.models import task as task_model  # noqa: F401
from app.repositories.tasks import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.services.tasks import (
    create_task as service_create_task,
)
from app.services.tasks import (
    get_task as service_get_task,
)

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def database_session() -> Generator[Session]:
    Base.metadata.create_all(bind=engine)

    with TestingSessionLocal() as session:

        def override_get_session() -> Generator[Session]:
            yield session

        app.dependency_overrides[get_session] = override_get_session
        yield session
        app.dependency_overrides.clear()

    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def assert_timestamp(value: str) -> None:
    assert isinstance(value, str)
    datetime.fromisoformat(value.replace("Z", "+00:00"))


def assert_task_payload(
    payload: dict[str, object],
    *,
    task_id: int,
    title: str,
    description: str | None,
    completed: bool,
) -> None:
    assert payload["id"] == task_id
    assert payload["title"] == title
    assert payload["description"] == description
    assert payload["completed"] is completed
    assert_timestamp(payload["created_at"])
    assert_timestamp(payload["updated_at"])


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover task creation and listing",
        },
    )

    assert response.status_code == 201
    assert_task_payload(
        response.json(),
        task_id=1,
        title="Write tests",
        description="Cover task creation and listing",
        completed=False,
    )


def test_create_task_without_description() -> None:
    response = client.post("/tasks", json={"title": "Ship API"})

    assert response.status_code == 201
    assert_task_payload(
        response.json(),
        task_id=1,
        title="Ship API",
        description=None,
        completed=False,
    )


def test_list_tasks() -> None:
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task", "description": "Later"})

    response = client.get("/tasks")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 2
    assert_task_payload(
        payload[0],
        task_id=1,
        title="First task",
        description=None,
        completed=False,
    )
    assert_task_payload(
        payload[1],
        task_id=2,
        title="Second task",
        description="Later",
        completed=False,
    )


def test_list_tasks_empty() -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


def test_list_tasks_supports_pagination() -> None:
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task"})
    client.post("/tasks", json={"title": "Third task"})

    response = client.get("/tasks?skip=1&limit=1")

    assert response.status_code == 200
    payload = response.json()
    assert len(payload) == 1
    assert_task_payload(
        payload[0],
        task_id=2,
        title="Second task",
        description=None,
        completed=False,
    )


def test_list_tasks_rejects_negative_skip() -> None:
    response = client.get("/tasks?skip=-1")

    assert response.status_code == 422


def test_get_task_by_id() -> None:
    create_response = client.post("/tasks", json={"title": "Read docs"})

    response = client.get(f"/tasks/{create_response.json()['id']}")

    assert response.status_code == 200
    assert_task_payload(
        response.json(),
        task_id=1,
        title="Read docs",
        description=None,
        completed=False,
    )


def test_get_task_by_id_returns_404() -> None:
    response = client.get("/tasks/999", headers={"X-Request-ID": "task-404"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
        "request_id": "task-404",
    }


def test_patch_task() -> None:
    create_response = client.post(
        "/tasks",
        json={
            "title": "Draft API docs",
            "description": "Initial version",
        },
    )

    response = client.patch(
        f"/tasks/{create_response.json()['id']}",
        json={
            "title": "Publish API docs",
            "description": None,
            "completed": True,
        },
    )

    assert response.status_code == 200
    assert_task_payload(
        response.json(),
        task_id=1,
        title="Publish API docs",
        description=None,
        completed=True,
    )


def test_patch_task_accepts_empty_body() -> None:
    create_response = client.post("/tasks", json={"title": "Leave unchanged"})

    response = client.patch(
        f"/tasks/{create_response.json()['id']}",
        json={},
    )

    assert response.status_code == 200
    assert_task_payload(
        response.json(),
        task_id=1,
        title="Leave unchanged",
        description=None,
        completed=False,
    )


def test_patch_task_rejects_null_title() -> None:
    create_response = client.post("/tasks", json={"title": "Keep title"})

    response = client.patch(
        f"/tasks/{create_response.json()['id']}",
        json={"title": None},
    )

    assert response.status_code == 422


def test_patch_task_returns_404() -> None:
    response = client.patch(
        "/tasks/999",
        json={"completed": True},
        headers={"X-Request-ID": "patch-404"},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
        "request_id": "patch-404",
    }


def test_delete_task() -> None:
    create_response = client.post("/tasks", json={"title": "Remove me"})
    task_id = create_response.json()["id"]

    delete_response = client.delete(f"/tasks/{task_id}")
    get_response = client.get(f"/tasks/{task_id}", headers={"X-Request-ID": "gone"})

    assert delete_response.status_code == 204
    assert delete_response.content == b""
    assert get_response.status_code == 404
    assert get_response.json() == {
        "detail": "Task not found",
        "request_id": "gone",
    }


def test_delete_task_returns_404() -> None:
    response = client.delete("/tasks/999", headers={"X-Request-ID": "delete-404"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Task not found",
        "request_id": "delete-404",
    }


def test_create_task_rejects_empty_title() -> None:
    response = client.post("/tasks", json={"title": ""})

    assert response.status_code == 422


def test_create_task_rejects_long_title() -> None:
    response = client.post("/tasks", json={"title": "x" * 101})

    assert response.status_code == 422


def test_create_task_rejects_long_description() -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Valid title",
            "description": "x" * 501,
        },
    )

    assert response.status_code == 422


def test_task_service_returns_created_task(database_session: Session) -> None:
    created_task = service_create_task(
        database_session,
        TaskCreate(title="Service task"),
    )

    fetched_task = service_get_task(database_session, created_task.id)

    assert fetched_task == created_task


def test_task_repository_updates_and_deletes_task(
    database_session: Session,
) -> None:
    repository = TaskRepository(database_session)
    repository_task = repository.create(TaskCreate(title="Repository task"))

    updated_task = repository.update(repository_task, TaskUpdate(completed=True))
    repository.delete(updated_task)

    assert updated_task.completed is True
    assert repository.get(updated_task.id) is None
