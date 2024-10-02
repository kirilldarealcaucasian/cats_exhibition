from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing_extensions import Literal

load_dotenv()


class Settings(BaseSettings):
    LOG_LEVEL: Literal["DEBUG", "WARNING", "INFO", "ERROR"] = "DEBUG"

    DB_USER: str
    DB_PASSWORD: str
    DB_SERVER: str
    DB_PORT: int
    DB_NAME: str

    @property
    def DB_URL(cls) -> str:  # noqa
        return f"postgresql+asyncpg://{cls.DB_USER}:{cls.DB_PASSWORD}@{cls.DB_SERVER}:{cls.DB_PORT}/{cls.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")


settings = Settings()
