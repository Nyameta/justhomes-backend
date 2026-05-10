from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    APP_NAME: str = "JustHomes AI"
    APP_ENV: str = "development"
    DEBUG: bool = True

    GROQ_API_KEY: str = ""
    GROQ_MODEL: str = "llama3-70b-8192"

    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
    ]

    COMPANY_NAME: str = "JustHomes"
    WHATSAPP_NUMBER: str = "+254700000000"
    AGENT_EMAIL: str = "agents@justhomes.co.ke"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()