from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    groq_api_key: Optional[str] = None

    class Config:
        env_file = "../.env" if os.path.exists("../.env") else None  # Load only if exists (local)

settings = Settings()