from pydantic_settings import BaseSettings

class Settings(BaseSettings):
   DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost/dbname"
   SECRET_KEY: str = "your_secret_key"

   class Config:
       env_file = ".env"

settings = Settings()