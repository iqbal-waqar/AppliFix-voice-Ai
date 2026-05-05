import os
from pydantic_settings import BaseSettings
from functools import lru_cache

_ENV_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), ".env")


class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:password@localhost:5432/voice_ai_db"

    vapi_api_key: str = ""
    vapi_phone_number_id: str = ""
    vapi_assistant_id: str = ""


    app_host: str = "0.0.0.0"
    app_port: int = 8000
    backend_url: str = "http://localhost:8000"

    class Config:
        env_file = _ENV_FILE
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
