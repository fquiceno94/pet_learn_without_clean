from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL:str 
    APP_ENV:str = "development"
    APP_NAME:str = "polymarket_intelligence"


settings = Settings()