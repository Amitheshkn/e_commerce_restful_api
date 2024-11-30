from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    MONGO_URI: str = Field(..., env="MONGO_URI")
    DATABASE_NAME: str = Field(..., env="DATABASE_NAME")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
