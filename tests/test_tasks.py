import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.db.session import get_session
from app.main import app
from app.models import task  # noqa: F401

engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(autouse=True)
def database_session() -> None:
    Base.metadata.create_all(bind=engine)

    def override_get_session() -> Session:
        with TestingSessionLocal() as session:
            yield session

    app.dependency_overrides[get_session] = override_get_session
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine)


client = TestClient(app)


def test_create_task() -> None:
    response = client.post(
        "/tasks",
        json={
            "title": "Write tests",
            "description": "Cover task creation and listing",
        },
    )

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Write tests",
        "description": "Cover task creation and listing",
        "completed": False,
    }


def test_create_task_without_description() -> None:
    response = client.post("/tasks", json={"title": "Ship API"})

    assert response.status_code == 201
    assert response.json() == {
        "id": 1,
        "title": "Ship API",
        "description": None,
        "completed": False,
    }


def test_list_tasks() -> None:
    client.post("/tasks", json={"title": "First task"})
    client.post("/tasks", json={"title": "Second task", "description": "Later"})

    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "First task",
            "description": None,
            "completed": False,
        },
        {
            "id": 2,
            "title": "Second task",
            "description": "Later",
            "completed": False,
        },
    ]


def test_list_tasks_empty() -> None:
    response = client.get("/tasks")

    assert response.status_code == 200
    assert response.json() == []


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
