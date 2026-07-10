from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Clinical Intelligence Copilot Platform"
    app_version: str = "0.1.0"
    app_description: str = "A personal healthcare document understanding platform."

    backend_host: str = "127.0.0.1"
    backend_port: int = 8000


settings = Settings()
