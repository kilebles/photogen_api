from urllib.parse import quote_plus
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_HOST: str
    APP_PORT: int
    APP_URL: str
    
    class Config:
            env_file = ".env"

     
config = Settings()