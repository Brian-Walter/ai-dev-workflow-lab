from fastapi import FastAPI

app = FastAPI(title="AI Dev Workflow Lab API")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/")
def root() -> dict[str, str]:
    return {"message": "AI Dev Workflow Lab API"}
