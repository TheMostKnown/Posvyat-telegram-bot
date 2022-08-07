from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = 'POSVYAT_TG'

    GOOGLE_TABLE_ID: Optional[str]
    GOOGLE_API_CREDS: Optional[str]
    GOOGLE_API_TOKEN: Optional[str]

    class Config:
        env_prefix = 'POSVYAT_'
        env_file = r'.env'
        env_file_encoding = 'utf-8'


settings = Settings()
