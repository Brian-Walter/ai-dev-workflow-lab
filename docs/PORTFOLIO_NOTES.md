# Portfolio Notes

## What This Project Is

AI Dev Workflow Lab is a small FastAPI backend built around a task management
API.

It is intended to show how a simple REST API can be organized, tested,
documented, containerized, and validated with CI in a professional development
workflow.

## Why The Domain Is Intentionally Simple

The task management domain is intentionally modest.

The goal is not to present a complex product, but to make the engineering
practices easy to inspect. A simple domain keeps attention on code structure,
API design, tests, Docker usage, logging, persistence, and automation.

## Engineering Practices Demonstrated

- Building REST endpoints with FastAPI
- Separating routes, schemas, services, repositories, models, database setup,
  and core infrastructure
- Validating request and response data with Pydantic
- Persisting data with SQLAlchemy and SQLite
- Managing database sessions through FastAPI dependencies
- Returning consistent error responses with request IDs
- Writing endpoint, service, and repository tests with Pytest
- Using Ruff for linting
- Running the API with Docker and Docker Compose
- Persisting SQLite data through a Docker Compose volume
- Running CI with GitHub Actions
- Documenting how to install, run, test, and evaluate the project

## Trade-Offs

- SQLite is used to keep the project easy to run locally and simple to review.
- Database tables are created with SQLAlchemy metadata instead of versioned
  migrations.
- Authentication and authorization are intentionally out of scope for this
  version.
- The API returns a plain list for task pagination instead of a richer response
  with metadata.
- The project favors readability and portfolio clarity over production-scale
  abstractions.

## Production-Grade Improvements

A production-grade version would likely add:

- Alembic migrations
- PostgreSQL or another production database
- authentication and authorization
- structured configuration loading per environment
- richer pagination metadata
- API versioning
- observability integrations
- deployment-specific settings
- stronger test coverage around failure modes and database behavior

These improvements are intentionally left out of the initial version to avoid
unnecessary complexity.

## How It Can Evolve Into A Small Business API

This codebase can evolve into a small business API by replacing the task domain
with real business entities such as clients, jobs, invoices, appointments,
inventory items, or support tickets.

The existing structure already separates HTTP routes, validation, business
logic, and persistence, which makes it a practical starting point for a small
internal tool or freelance backend foundation.
