from pydantic_settings import BaseSettings
from typing import List, Optional
import secrets
from datetime import datetime

class Settings(BaseSettings):
    # Basic Config
    PROJECT_NAME: str = "Building Management System"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    # CORS Settings
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:8000", "http://localhost:3000"]

    # Database Settings
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    DATABASE_URI: Optional[str] = None

    # App Settings
    BUILDING_NAME: str = "Sample Building"
    ADMIN_EMAIL: str = "admin@example.com"
    WARM_MONTHS: List[int] = [4, 5, 6, 7, 8, 9]  # Farvardin to Shahrivar
    COLD_MONTHS: List[int] = [10, 11, 12, 1, 2, 3]  # Mehr to Esfand

    class Config:
        case_sensitive = True
        env_file = "../.env"

    @property
    def async_database_url(self):
        return f"postgresql+asyncpg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}/{self.POSTGRES_DB}"

settings = Settings()
