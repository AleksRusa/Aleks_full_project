from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import BaseModel, Field

class AuthJWT(BaseModel):
    private_key_path: Path = Path("src/certs/jwt-private.pem")
    public_key_path: Path = Path("src/certs/jwt-public.pem")
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 15

class Redis(BaseSettings):
    host: str = Field(alias="REDIS_HOST")
    port: int = Field(alias="REDIS_PORT")
    db: int = Field(alias="REDIS_DB")

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    redis: Redis
    auth_jwt: AuthJWT = AuthJWT()

    model_config = SettingsConfigDict(
        env_file=".env", 
        env_file_encoding="utf-8", 
        env_nested_delimiter="__"
    )

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
    
    @property
    def redis_url_aioredis(self):
        return f"redis://{self.redis.host}:{self.redis.port}/{self.redis.db}"

# Создание экземпляра настроек
settings = Settings()
