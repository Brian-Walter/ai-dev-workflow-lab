# ai-dev-workflow-lab

API Python minima criada com FastAPI.

## Requisitos

- Python 3.12 ou 3.13

## Instalacao

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Executar a API

```powershell
python -m uvicorn app.main:app --reload --app-dir src
```

Endpoints disponiveis:

- `GET /` retorna `{"message": "AI Dev Workflow Lab"}`
- `GET /health` retorna `{"status": "ok"}`

## Docker

Build da imagem:

```powershell
docker build -t ai-dev-workflow-lab .
```

Executar com Docker:

```powershell
docker run --rm -p 8000:8000 ai-dev-workflow-lab
```

Executar ambiente local com Docker Compose:

```powershell
docker compose up --build
```

A API fica disponivel em `http://localhost:8000`.

## Testes e lint

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

O script instala as dependencias de desenvolvimento no `.venv` local e executa:

- `python -m ruff check .`
- `python -m pytest -q`
