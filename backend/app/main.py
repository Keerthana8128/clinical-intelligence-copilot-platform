from fastapi import FastAPI

app = FastAPI(
    title="Clinical Intelligence Copilot Platform",
    description="A personal healthcare document understanding platform.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Clinical Intelligence Copilot Platform API is running",
        "status": "healthy",
        "version": "0.1.0"
    }


@app.get("/health")
def health_check():
    return {
        "status": "ok"
    }