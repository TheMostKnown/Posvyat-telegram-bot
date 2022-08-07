from pydantic import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = 'POSVYAT_TG'

    TG_TOKEN: Optional[str]

    GOOGLE_TABLE_ID: Optional[str]
    GOOGLE_CREDS_PATH: Optional[str]
    GOOGLE_TOKEN_PATH: Optional[str]

    class Config:
        env_prefix = 'POSVYAT_TG_'
        env_file = r'C:\Users\user\PycharmProjects\posvyatTg\tgbot\.env'
        env_file_encoding = 'utf-8'
        fields = {
            'GOOGLE_TABLE_ID': {'env': 'GOOGLE_TABLE_ID'},
            'GOOGLE_CREDS_PATH': {'env': 'GOOGLE_CREDS_PATH'},
            'GOOGLE_TOKEN_PATH': {'env': 'GOOGLE_TOKEN_PATH'}
        }


settings = Settings()
