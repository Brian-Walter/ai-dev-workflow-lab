# AI Dev Workflow Lab

API Python com FastAPI criada para praticar um fluxo moderno de desenvolvimento:
arquitetura modular, testes automatizados, lint, persistencia SQLite, Docker,
logging estruturado e automacoes de CI.

## Stack

- Python 3.12 ou 3.13
- FastAPI
- Uvicorn
- Pydantic
- SQLAlchemy
- SQLite
- Pytest
- Ruff
- Docker e Docker Compose
- GitHub Actions

## Estrutura do Projeto

```text
.
├── .github/workflows/      # Workflows de CI e review automatizado
├── scripts/                # Scripts de automacao local
├── src/app/
│   ├── api/                # Rotas HTTP
│   ├── core/               # Configuracao, logging, middleware e exceptions
│   ├── db/                 # Engine, sessoes e setup/migracoes simples
│   ├── models/             # Modelos SQLAlchemy
│   ├── repositories/       # Acesso ao banco de dados
│   ├── schemas/            # Schemas Pydantic
│   ├── services/           # Regras de aplicacao
│   └── main.py             # Factory da aplicacao FastAPI
├── tests/                  # Testes automatizados
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Requisitos

- Python 3.12 ou 3.13
- PowerShell
- Git
- Docker, opcional para execucao containerizada

## Instalacao Local

Crie e ative o ambiente virtual:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Instale a aplicacao com dependencias de desenvolvimento:

```powershell
python -m pip install -e ".[dev]"
```

## Execucao Local

Inicie a API em modo desenvolvimento:

```powershell
python -m uvicorn app.main:app --reload --app-dir src
```

A API ficara disponivel em:

```text
http://localhost:8000
```

A documentacao interativa do FastAPI fica em:

```text
http://localhost:8000/docs
```

## Execucao com Docker

Build da imagem:

```powershell
docker build -t ai-dev-workflow-lab .
```

Executar com Docker:

```powershell
docker run --rm -p 8000:8000 ai-dev-workflow-lab
```

Executar com Docker Compose:

```powershell
docker compose up --build
```

## Testes e Lint

Execute a validacao local completa:

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\check.ps1
```

O script:

- cria ou reutiliza o `.venv` local;
- instala o projeto com `python -m pip install -e ".[dev]"`;
- executa `python -m ruff check .`;
- executa `python -m pytest -q`.

## Endpoints Disponiveis

| Metodo | Rota | Descricao |
| --- | --- | --- |
| `GET` | `/` | Retorna a mensagem principal da API |
| `GET` | `/health` | Retorna o status de saude da API |
| `POST` | `/tasks` | Cria uma task |
| `GET` | `/tasks` | Lista tasks |

Exemplo de criacao de task:

```json
{
  "title": "Write tests",
  "description": "Cover task creation and listing"
}
```

Resposta:

```json
{
  "id": 1,
  "title": "Write tests",
  "description": "Cover task creation and listing",
  "completed": false
}
```

## Fluxo de Desenvolvimento

1. Atualize a branch principal.
2. Crie uma branch curta e descritiva.
3. Implemente mudancas pequenas e focadas.
4. Rode lint e testes localmente.
5. Revise o diff antes do commit.
6. Abra um pull request.
7. Aguarde CI, review automatizado e revisao humana.

## Comandos Git Recomendados

Atualizar a branch principal:

```powershell
git checkout main
git pull
```

Criar uma branch de trabalho:

```powershell
git checkout -b feature/task-endpoints
```

Revisar alteracoes:

```powershell
git status
git diff
```

Commitar:

```powershell
git add .
git commit -m "Describe the change"
```

Enviar para o remoto:

```powershell
git push -u origin feature/task-endpoints
```

## Proximos Passos

- Adicionar Alembic para migracoes versionadas.
- Implementar `GET /tasks/{id}`, `PATCH /tasks/{id}` e `DELETE /tasks/{id}`.
- Adicionar configuracao por ambiente para banco, log level e modo de execucao.
- Persistir o SQLite em volume dedicado no Docker Compose.
- Expandir a cobertura de testes para repositories e services.
