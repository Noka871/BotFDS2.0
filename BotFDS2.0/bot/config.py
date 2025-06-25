# Конфигурация бота
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    ADMIN_IDS: list[int]
    DB_URL: str = "sqlite:///data/database.db"

    class Config:
        env_file = ".env"


config = Settings()