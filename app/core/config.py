from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    MYSQL_HOST: str = "localhost"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str
    MYSQL_NAME: str

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
