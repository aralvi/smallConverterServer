from pydantic import BaseSettings, AnyHttpUrl
from typing import List
from decouple import config


class Settings(BaseSettings):
    API: str = "/api"
    JWT_SECRET: str = config("JWT_SECRET", cast=str)
    MONGO_URI: str = config("MONGO_URI", cast=str)
    MAIL: str = config("MAIL", cast=str)
    MAIL_PASS: str = config("MAIL_PASS", cast=str)
    TOKEN_EXPIRES_IN_MINUTES: int = 60 * 24 * 5  # 5 days
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:1512",
        "http://127.0.0.1:5173"
    ]
    PROJECT_NAME: str = "SmallConverterTools Api"
    PROJECT_URL: str = config("PROJECT_URL", cast=str)

    class Config:
        case_sensitive = True


settings = Settings()
