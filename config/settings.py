# config/settings.py
from typing import Optional

from pydantic import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./test.db"
    s3_bucket: str
    broker_url: str = "redis://localhost:6379/0"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None
    aws_region: str = "us-east-1"

    class Config:
        env_file = ".env"


settings = Settings()
