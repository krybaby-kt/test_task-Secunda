from pydantic_settings import BaseSettings, SettingsConfigDict


__env_file__: str = ".env.test"


class Settings(BaseSettings):
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USERNAME: str
    DATABASE_PASSWORD: str
    DATABASE_NAME: str
    
    BACKEND_HOST: str
    BACKEND_PORT: int

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    @property
    def DATABASE_URL_psycopg(self):
        return f"postgresql+psycopg://{self.DATABASE_USERNAME}:{self.DATABASE_PASSWORD}@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
    
    model_config = SettingsConfigDict(env_file=__env_file__)


settings = Settings()
