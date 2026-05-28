# AI Dev Workflow Lab

[![CI](https://github.com/Brian-Walter/ai-dev-workflow-lab/actions/workflows/ci.yml/badge.svg)](https://github.com/Brian-Walter/ai-dev-workflow-lab/actions/workflows/ci.yml)

AI Dev Workflow Lab is a Python/FastAPI backend project designed to practice and demonstrate professional software engineering workflows through a simple task management API. It includes modular architecture, automated tests, SQLite persistence, Docker support, structured logging, linting, and CI automation.

## Overview

This project exposes a small REST API for managing tasks. The domain is intentionally simple so the repository can focus on backend engineering practices: clear module boundaries, predictable validation, database access through repositories, service-level application logic, testable endpoints, Dockerized execution, and GitHub Actions automation.

The API supports creating, listing, reading, updating, and deleting tasks. It also includes health and root endpoints, request ID propagation, structured JSON logs, and consistent error responses.

Interactive API documentation is available at:

```text
http://localhost:8000/docs
```

## Features

- REST API built with FastAPI
- Task CRUD endpoints
- Simple pagination for task listing
- SQLite persistence with SQLAlchemy
- Pydantic request and response schemas
- Modular route, schema, service, repository, model, database, and core layers
- Structured JSON request logging
- Request ID propagation through `X-Request-ID`
- Consistent error responses with request IDs
- Automated tests with Pytest
- Ruff linting
- Dockerfile and Docker Compose support
- SQLite persistence through a Docker Compose volume
- GitHub Actions workflow for linting, tests, and Docker image build
- Automated PR review workflow for lint/test summaries and common repository checks

## Tech Stack

- Python 3.12+
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Ruff
- Docker and Docker Compose
- GitHub Actions

## Architecture

The project uses a small layered architecture:

- `api`: HTTP routes and FastAPI-specific request handling.
- `schemas`: Pydantic models for request validation and response serialization.
- `services`: Application logic and use-case orchestration.
- `repositories`: SQLAlchemy database access.
- `models`: SQLAlchemy ORM models.
- `db`: Engine, sessions, and lightweight table creation.
- `core`: Configuration, logging, middleware, request context, and exception handling.

This keeps the API easy to understand while still demonstrating separation of concerns. Routes stay thin, services coordinate behavior, repositories own persistence details, and schemas define the public API contract.

## Project Structure

```text
.
|-- .github/workflows/      # CI and automated PR review workflows
|-- scripts/                # Local development scripts
|-- src/app/
|   |-- api/                # FastAPI routes
|   |-- core/               # Config, logging, middleware, exceptions
|   |-- db/                 # SQLAlchemy engine, sessions, table setup
|   |-- models/             # SQLAlchemy ORM models
|   |-- repositories/       # Database access layer
|   |-- schemas/            # Pydantic schemas
|   |-- services/           # Application logic
|   `-- main.py             # FastAPI application factory
|-- tests/                  # Automated tests
|-- .env.example            # Example environment configuration
|-- Dockerfile
|-- docker-compose.yml
|-- LICENSE
|-- pyproject.toml
`-- README.md
```

## API Endpoints

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/` | Returns the API message |
| `GET` | `/health` | Returns the health status |
| `POST` | `/tasks` | Creates a task |
| `GET` | `/tasks?skip=0&limit=100` | Lists tasks with simple pagination |
| `GET` | `/tasks/{task_id}` | Returns a single task |
| `PATCH` | `/tasks/{task_id}` | Updates a task |
| `DELETE` | `/tasks/{task_id}` | Deletes a task |

Pagination rules:

- `skip` must be greater than or equal to `0`.
- `limit` must be between `1` and `100`.

## Request and Response Examples

Create a task:

```bash
curl -X POST http://localhost:8000/tasks \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"Write tests\",\"description\":\"Cover task creation and listing\"}"
```

Response:

```json
{
  "id": 1,
  "title": "Write tests",
  "description": "Cover task creation and listing",
  "completed": false
}
```

List tasks:

```bash
curl "http://localhost:8000/tasks?skip=0&limit=10"
```

Response:

```json
[
  {
    "id": 1,
    "title": "Write tests",
    "description": "Cover task creation and listing",
    "completed": false
  }
]
```

Get a task by ID:

```bash
curl http://localhost:8000/tasks/1
```

Update a task:

```bash
curl -X PATCH http://localhost:8000/tasks/1 \
  -H "Content-Type: application/json" \
  -d "{\"completed\":true}"
```

Response:

```json
{
  "id": 1,
  "title": "Write tests",
  "description": "Cover task creation and listing",
  "completed": true
}
```

Delete a task:

```bash
curl -X DELETE http://localhost:8000/tasks/1
```

Missing task response:

```json
{
  "detail": "Task not found",
  "request_id": "request-id-value"
}
```

## Running Locally

Create and activate a virtual environment:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install the project with development dependencies:

```powershell
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Use `.env.example` as a reference for supported environment variables. For local runs, set variables in your shell before starting the API when you need to override defaults:

```powershell
$env:DATABASE_URL = "sqlite:///./app.db"
$env:LOG_LEVEL = "INFO"
```

Run the API:

```powershell
python -m uvicorn app.main:app --reload --app-dir src
```

Open:

```text
http://localhost:8000
http://localhost:8000/docs
```

Environment variables:

| Variable | Default | Description |
| --- | --- | --- |
| `APP_ENV` | `development` | Application environment label |
| `APP_TITLE` | `AI Dev Workflow Lab API` | FastAPI application title |
| `DATABASE_URL` | `sqlite:///./app.db` | SQLAlchemy database URL |
| `LOG_LEVEL` | `INFO` | Root logging level |

## Running with Docker

Build the image:

```powershell
docker build -t ai-dev-workflow-lab .
```

Run the container with a persistent SQLite volume:

```powershell
docker volume create ai-dev-workflow-lab-data
docker run --rm -p 8000:8000 `
  -e DATABASE_URL=sqlite:////data/app.db `
  -v ai-dev-workflow-lab-data:/data `
  ai-dev-workflow-lab
```

Run with Docker Compose:

```powershell
docker compose up --build
```

Docker Compose mounts the source code for local development and stores SQLite data in the `sqlite_data` named volume.

## Tests and Code Quality

Run lint:

```powershell
python -m ruff check .
```

Run tests:

```powershell
python -m pytest -q
```

Run the local validation script:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

The script creates or reuses `.venv`, installs development dependencies, runs Ruff, and runs Pytest.

## Development Workflow

The repository is intended to model a small but professional backend workflow:

1. Create a short feature branch.
2. Make focused changes.
3. Add or update tests for behavior changes.
4. Run lint and tests locally.
5. Review the diff before committing.
6. Open a pull request.
7. Let CI validate lint, tests, and Docker build.

## Continuous Integration

The main CI workflow runs on pushes and pull requests. It:

- checks out the repository;
- installs Python 3.13;
- installs the project with development dependencies;
- runs `python -m ruff check .`;
- runs `python -m pytest -q`;
- builds the Docker image.

The PR review workflow adds an automated pull request comment with lint output, test output, and common repository checks such as generated artifacts, debug statements, and missing Docker files.

## Roadmap

- Add Alembic for versioned database migrations.
- Add filtering by task status.
- Add pagination metadata for list responses.
- Add authentication as a separate future exercise.
- Add production database examples such as PostgreSQL.
- Add more OpenAPI examples and API contract documentation.
- Add coverage reporting.

## What This Project Demonstrates

This project demonstrates backend skills that are useful for junior backend roles, freelance API work, and professional portfolio review:

- Building REST APIs with FastAPI
- Structuring backend applications
- Separating routes, schemas, services, repositories, and models
- Validating data with Pydantic
- Persisting data with SQLAlchemy and SQLite
- Managing database sessions through FastAPI dependencies
- Returning consistent error responses
- Writing automated tests with Pytest
- Testing endpoints, services, and repositories
- Using Ruff for linting
- Running applications with Docker
- Persisting local container data with Docker Compose volumes
- Setting up CI workflows with GitHub Actions
- Following a small but professional development workflow

Learning goals:

- Practice clean backend boundaries without overengineering.
- Build confidence with automated validation before publishing code.
- Show how a simple API can still use maintainable engineering habits.

Freelance relevance:

- The project shows how to deliver a small API with documentation, validation, tests, Docker support, and CI.
- The structure can be adapted for client projects that need CRUD APIs, internal tools, or backend foundations.

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
