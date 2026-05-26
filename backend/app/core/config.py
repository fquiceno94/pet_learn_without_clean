from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")
    DATABASE_URL:str 
    APP_ENV:str = "development"
    APP_NAME:str = "polymarket_intelligence"
    GAMMA_API_URL:str = "https://gamma-api.polymarket.com"


settings = Settings()