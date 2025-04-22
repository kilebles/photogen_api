from urllib.parse import quote_plus
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    APP_URL: str
    
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASS: str
    
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    TG_BOT_TOKEN: str
    
    REPLICATE_TOKEN: str
    REPLICATE_WEBHOOK_SECRET: str
    REPLICATE_API_URL: str
    REPLICATE_MODEL_VERSION: str
    REPLICATE_TRAIN_VERSION: str
    REPLICATE_GEN_VERSION: str
    REPLICATE_FACE_SWAP_VERSION: str
    REPLICATE_CLAUDE_MODEL: str
    REPLICATE_MODEL_SLUG: str
    REPLICATE_TRAIN_OWNER: str

    @property
    def DATABASE_URL(self) -> str:
        encoded_pass = quote_plus(self.DB_PASS)
        return f"postgres://{self.DB_USER}:{encoded_pass}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file=".env")
     
     
config = Settings()

TORTOISE_ORM = {
    "connections": {
        "default": config.DATABASE_URL,
    },
    "apps": {
        "models": {
            "models": ["photogen_api.database.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}