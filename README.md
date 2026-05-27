# ai-dev-workflow-lab

API Python mínima criada com FastAPI.

## Requisitos

- Python 3.11+

## Instalação

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -e ".[dev]"
```

## Executar a API

```powershell
python -m uvicorn app.main:app --reload --app-dir src
```

Endpoints disponíveis:

- `GET /`
- `GET /health`

## Verificações

```powershell
.\scripts\check.ps1
```

O script executa:

- `ruff check .`
- `pytest`
