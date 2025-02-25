from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel

class AuthJWT(BaseModel):
    private_key_path: Path = Path("certs/jwt-private.pem")
    public_key_path: Path = Path("certs/jwt-public.pem")
    algorithm: str = "RS256"

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    auth_jwt: AuthJWT = AuthJWT()

# Создание экземпляра настроек
settings = Settings()
