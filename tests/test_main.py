from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


@app.get("/test-error", include_in_schema=False)
def raise_test_error() -> None:
    raise RuntimeError("test error")


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_root_returns_message() -> None:
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "AI Dev Workflow Lab"}


def test_request_id_is_generated() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.headers["X-Request-ID"]


def test_request_id_is_preserved() -> None:
    response = client.get("/health", headers={"X-Request-ID": "request-123"})

    assert response.status_code == 200
    assert response.headers["X-Request-ID"] == "request-123"


def test_not_found_response_includes_request_id() -> None:
    response = client.get("/missing", headers={"X-Request-ID": "missing-123"})

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Not Found",
        "request_id": "missing-123",
    }


def test_unhandled_exception_response_includes_request_id() -> None:
    error_client = TestClient(app, raise_server_exceptions=False)

    response = error_client.get(
        "/test-error",
        headers={"X-Request-ID": "error-123"},
    )

    assert response.status_code == 500
    assert response.json() == {
        "detail": "Internal server error",
        "request_id": "error-123",
    }
