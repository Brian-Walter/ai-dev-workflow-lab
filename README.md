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

## Testes e lint

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

O script instala as dependencias de desenvolvimento no `.venv` local e executa:

- `python -m ruff check .`
- `python -m pytest -q`
